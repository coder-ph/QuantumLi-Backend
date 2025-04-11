from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, decode_token, get_jwt_identity
from datetime import timedelta
from src.utils.logger import logger  
from src.config.redis_config import init_redis
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from src.utils.email_util import send_email
from werkzeug.security import check_password_hash
from src.error.apiErrors import InternalServerError, ConflictError, UnauthorizedError
from src.Models.systemusers import System_Users

from src.startup.database import db

REVOCATION_KEY_PREFIX = "revoked_tokens"
BASE_URL = "http://localhost:5555/auth"

def generate_tokens(user, access_token_expiry_hours=1, roles=None):
    try:
        roles = roles or []

        additional_claims = {
            "roles": roles,
            "user_id": user.id  
        }

        access_token = create_access_token(
            identity=user.id, 
            fresh=True, 
            expires_delta=timedelta(hours=access_token_expiry_hours),
            additional_claims=additional_claims
        )

        refresh_token = create_refresh_token(identity=user.id)

        logger.info(f"Generated tokens for user {user.id}, roles: {roles}")

        return access_token, refresh_token
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while generating tokens for user {user.id}: {str(db_error)}")
        return None
    
    except Exception as e:
        logger.error(f"Unexpected error occurred while generating tokens for user {user.id}: {str(e)}")
        return None


def revoke_token(token, expires_in):

    try:
        if not token:
            logger.warning("Token is missing or invalid.")
            raise ValueError("Token is required.")
        
        if expires_in <= 0:
            logger.warning(f"Invalid expiration time: {expires_in}. Must be greater than zero.")
            raise ValueError("Expiration time must be greater than zero.")
       
        max_ttl = 3600  # 1 hour max TTL
        if expires_in > max_ttl:
            logger.warning(f"Expires in too long: {expires_in}. Consider reducing the TTL.")
            raise ValueError(f"Expires in is too long. Maximum allowed is {max_ttl} seconds.")
        
        jti = get_jti(token)
        if not jti:
            logger.warning("Failed to retrieve JTI from the token.")
            raise ValueError("Invalid token. No JTI found.")
        
        key = f"{REVOCATION_KEY_PREFIX}:{jti}"
        
        init_redis.redis_client.setex(key, timedelta(seconds=expires_in), "revoked")
        logger.info(f"Token revoked | jti: {jti} | expires_in: {expires_in}s")
        
        return True
    except ValueError as e:
        logger.warning(f"Invalid input | Reason: {str(e)}")
        return False
    except Exception as e:
        logger.exception(f"Failed to revoke token | Reason: {str(e)}")
        return False


def hash_password(password):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        logger.info(f"Password hashed successfully.")
        return hashed_password
    except Exception as e:
        logger.error(f"Error while hashing password: {str(e)}")
        raise


def verify_password(stored_password, provided_password):
    try:
        if bcrypt.checkpw(provided_password.encode('utf-8'), stored_password):
            logger.info(f"Password verification successful.")
            return True
        else:
            logger.warning(f"Password verification failed.")
            return False
    except Exception as e:
        logger.error(f"Error while verifying password: {str(e)}")
        return False
    
def create_user(validated_data, hashed_pw):
    from src.Models.systemusers import System_Users
    try:
        
        existing_user = System_Users.query.filter_by(email=validated_data['email']).first()
        if existing_user:
            logger.warning(f"Signup failed: Email already exists - {validated_data['email']}")
            raise ConflictError("Email is already registered.")


        new_user = System_Users(
            email=validated_data['email'].strip().lower(),
            password_hash=hashed_pw,  
            phone = validated_data['phone'],
            username=validated_data['username'].strip(),
            role=validated_data['role'].strip(),
            status='pending_verification'  
        )

        
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"New user created: {new_user.email}, status: {new_user.status}")

        return new_user

    except SQLAlchemyError as db_error:
        db.session.rollback()
        logger.error(f"Database error while creating user: {str(db_error)}")
        raise InternalServerError("Database error occurred during user creation.")
    except Exception as e:
        logger.error(f"Unexpected error during user creation: {str(e)}")
        raise InternalServerError("An unexpected error occurred during user creation.")


def create_verification_token(user):
    try:
       
        token = create_access_token(identity=user.user_id, expires_delta=timedelta(hours=24))
        logger.info(f"Generated verification token for user {user.email}")
        return token
    except Exception as e:
        logger.error(f"Error generating verification token: {str(e)}")
        raise InternalServerError("An error occurred while generating the verification token.")

def send_verification_email(email, token):
    try:
        
        verification_link = f"{BASE_URL}/verify-email?token={token}"
        subject = "Email Verification"
        body = f"Hello, please click on the link to verify your email: {verification_link}"
        
        
        send_email(subject, body, email)
        logger.info(f"Verification email sent to {email}")
    
    except Exception as e:
        logger.error(f"Error sending verification email to {email}: {str(e)}")
        raise InternalServerError("An error occurred while sending the verification email.")



def get_current_user():
    
    user_id = get_jwt_identity()  
    if not user_id:
        raise UnauthorizedError("User is not authenticated.")
    
    user = System_Users.query.get(user_id)  
    if not user:
        raise UnauthorizedError("User not found.")
    
    return user


def decode_verification_token(token):
    try:
        
        decoded_token = decode_token(token)
        return decoded_token
    except Exception as e:
        logger.error(f"Error decoding verification token: {str(e)}")
        raise InternalServerError("Failed to decode the verification token.")

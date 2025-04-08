from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from datetime import timedelta
from src.utils.logger import logger  
from src.config.redis_config import init_redis
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from werkzeug.security import check_password_hash

REVOCATION_KEY_PREFIX = "revoked_tokens"

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
       
        max_ttl = 3600  
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

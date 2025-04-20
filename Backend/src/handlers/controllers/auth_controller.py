from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, exceptions, decode_token
from src.services.auth_service import verify_password, generate_tokens, revoke_token
from src.Models.systemusers import System_Users
from src.Models.audit_logs import Audit_Logs
from src.utils.rate_limiter import limiter
from src.utils.logger import logger
from src.error.apiErrors import ValidationError, UnauthorizedError, InternalServerError
import redis
import json
from src.services.auth_service import hash_password, create_user, send_verification_email, create_verification_token
from src.utils.audit_logger import log_audit_event
from datetime import datetime
import uuid
from src.startup.database import db
from src.error.apiErrors import ValidationError, InternalServerError, ConflictError
from src.services_layer.validators.auth_validators import SignUpSchema
from src.services.auth_service import hash_password
from sqlalchemy.exc import IntegrityError

def get_redis_client():
    try:
        return redis.StrictRedis(
            host=current_app.config.get("REDIS_HOST", "localhost"),
            port=current_app.config.get("REDIS_PORT", 6379),
            db=current_app.config.get("REDIS_DB", 0),
            decode_responses=True
        )
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        raise InternalServerError("Server configuration error.")

@limiter.limit("5 per minute")
def login():
    try:
        data = request.get_json()
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'unknown')

        if not data or not data.get('email') or not data.get('password'):
            logger.warning(f"Login attempt missing credentials | IP: {user_ip} | Agent: {user_agent}")
            raise ValidationError("Email and password are required.")

        logger.debug(f"Login data received: {data}")

        user = System_Users.query.filter_by(email=data['email']).first()

        if not user:
            logger.warning(f"Login failed: User not found | Email: {data['email']} | IP: {user_ip}")
            raise UnauthorizedError("Invalid credentials.")

  
        try:
            user_uuid = uuid.UUID(str(user.user_id))
        except (ValueError, AttributeError) as e:
            logger.error(f"Invalid user_id format: {user.user_id} | Error: {str(e)}")
            raise InternalServerError("System data integrity error")

        if not verify_password(user.password_hash, data['password']):
            logger.warning(f"Login failed: Invalid password | User ID: {user.user_id} | IP: {user_ip}")
            raise UnauthorizedError("Invalid credentials.")

        roles = user.role
        access_token, refresh_token = generate_tokens(user, roles=roles)

        user_session_data = {
            "user_id": str(user.user_id),
            "email": user.email,
            "role": user.role if hasattr(user, "role") else "user",
            "ip": user_ip,
            "user_agent": user_agent,
        }

        redis_client = get_redis_client()
        redis_key = f"user_session:{user.user_id}"
        redis_client.set(redis_key, json.dumps(user_session_data), ex=60 * 60 * 2)

        audit_log = Audit_Logs(
            user_id=user.user_id,
            action_type="login",
            affected_table="users",
            record_id=user.user_id,
            timestamp=datetime.utcnow(),
            ip_address=user_ip,
            user_agent=user_agent
        )
        db.session.add(audit_log)
        db.session.commit()

        logger.info(f"User login successful | ID: {user.user_id} | IP: {user_ip} | Agent: {user_agent}")

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    except (ValidationError, UnauthorizedError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)} | IP: {request.remote_addr}")
        raise InternalServerError("An unexpected error occurred. Please try again later.")

@jwt_required()
def logout():
    try:
        jwt_payload = get_jwt()
        jti = jwt_payload["jti"]
        exp_timestamp = jwt_payload["exp"]
        now = datetime.utcnow().timestamp()
        ttl = int(exp_timestamp - now)

        if ttl <= 0:
            return jsonify({"message": "Token already expired"}), 400

        revoked = revoke_token(jwt_payload, ttl)
        if revoked:
            return jsonify({"message": "Successfully logged out"}), 200
        else:
            return jsonify({"message": "Failed to revoke token"}), 500

    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500
   
@limiter.limit("5 per minute")  
def signup():
    try:
        
        data = request.get_json()
        if not data:
            logger.warning("Signup request without JSON body.")
            raise ValidationError("Missing JSON body.")
        
        schema = SignUpSchema()
        validated_data = schema.load(data)

        email = validated_data["email"].strip().lower()
        phone = validated_data["phone"].strip()

        existing_user = System_Users.query.filter_by(email=email).first()
        if existing_user:
            logger.warning(f"Signup failed: Email already exists - {email}")
            raise ConflictError("Email is already registered.")

        hashed_pw = hash_password(validated_data["password"])

        new_user = create_user(validated_data, hashed_pw)

        verification_token = create_verification_token(new_user)
        send_verification_email(new_user.email, verification_token)

        redis_client = get_redis_client()
        redis_client.set(f"email_verification:{new_user.user_id}", verification_token, ex=60 * 60 * 24)  # expires in 24 hours

        logger.info(f"New user created and verification email sent | email: {new_user.email}, id: {new_user.user_id}")
        
        log_audit_event(user_id=new_user.user_id, action="signup", ip=request.remote_addr, user_agent=request.headers.get("User-Agent"))

        return jsonify({"message": "User registered successfully. Please verify your email."}), 201

    except ValidationError as ve:
        logger.warning(f"Validation error on signup: {ve.messages}")
        raise ve

    except IntegrityError as db_err:
        db.session.rollback()
        logger.error(f"Database IntegrityError during signup: {str(db_err)}")
        raise ConflictError("User with this email already exists.")

    except Exception as e:
        logger.exception(f"Unexpected server error during signup: {str(e)}")
        raise InternalServerError("Something went wrong. Please try again later.")

def verify_email():
    try:
        token = request.args.get('token')  

        if not token:
            logger.warning("Verification failed: Missing token in the request.")
            raise ValidationError("Token is required to verify the email.")

        try:
            decoded_token = decode_token(token)
            print(decoded_token)
            user_id = decoded_token['sub']
            logger.info("user verified  ")
        except exceptions.RevokedTokenError:
            logger.warning("Verification failed: Token has expired.")
            raise ValidationError("The verification token has expired.")
        except exceptions.JWTExtendedException:
            logger.warning("Verification failed: Invalid token.")
            raise ValidationError("Invalid token. Please request a new verification email.")

        user_id = uuid.UUID(user_id)
        user = System_Users.query.get(user_id)
        if not user:
            logger.warning(f"Verification failed: User not found with ID: {user_id}")
            raise ValidationError("User not found.")

        if user.status == 'active':
            logger.info(f"User {user_id} is already verified and attempted another verification.")
            return jsonify({"message": "User is already verified."}), 200

        user.status = 'active'
        db.session.commit()
        
        redis_client = get_redis_client()
        redis_key = f"email_verification:{user.user_id}"
        if redis_client.exists(redis_key):
            redis_client.delete(redis_key)
            logger.info(f"Deleted Redis entry for email verification of user {user_id}. Token can no longer be reused.")

        logger.info(f"User {user_id} verified successfully at {datetime.utcnow()}.")

        return jsonify({"message": "Email verified successfully. You can now log in."}), 200

    except ValidationError as ve:
       
        logger.warning(f"Validation error during email verification: {str(ve)}")
        raise ve
    except Exception as e:
        
        logger.error(f"Unexpected error during email verification: {str(e)}")
        raise InternalServerError("An error occurred during email verification.")
from flask import request, jsonify, current_app
from src.services.auth_service import verify_password, generate_tokens
from src.Models.systemusers import System_Users
from src.utils.rate_limiter import limiter
from src.utils.logger import logger
from src.error.apiErrors import ValidationError, UnauthorizedError, InternalServerError
import redis
import json

# Initialize Redis client using app config
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

        user = System_Users.query.filter_by(email=data['email']).first()

        if not user:
            logger.warning(f"Login failed: User not found | Email: {data['email']} | IP: {user_ip}")
            raise UnauthorizedError("Invalid credentials.")

        if not verify_password(user.password, data['password']):
            logger.warning(f"Login failed: Invalid password | User ID: {user.id} | IP: {user_ip}")
            raise UnauthorizedError("Invalid credentials.")

        
        access_token, refresh_token = generate_tokens(user)

        # user session data
        user_session_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role if hasattr(user, "role") else "user",
            "ip": user_ip,
            "user_agent": user_agent,
        }

       
        redis_client = get_redis_client()
        redis_key = f"user_session:{user.id}"
        redis_client.set(redis_key, json.dumps(user_session_data), ex=60 * 60 * 2)  

        logger.info(f"User login successful | ID: {user.id} | IP: {user_ip} | Agent: {user_agent}")

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    except (ValidationError, UnauthorizedError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)} | IP: {request.remote_addr}")
        raise InternalServerError("An unexpected error occurred. Please try again later.")

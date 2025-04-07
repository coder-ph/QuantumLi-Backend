from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from src.utils.logger import logger  
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from werkzeug.security import check_password_hash

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

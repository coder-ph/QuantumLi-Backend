
from src.Models.systemusers import System_Users
from src.startup.database import db
from src.utils.logger import logger
from src.error.apiErrors import InternalServerError

def get_user_by_username(username):
    try:
        if not username or not isinstance(username, str):
            logger.warning("get_user_by_username: Invalid username input.")
            return None

        sanitized_username = username.strip()
        user = db.session.query(System_Users).filter_by(username=sanitized_username).first()

        if user:
            logger.debug(f"User found with username: {sanitized_username}")
        else:
            logger.info(f"No user found with username: {sanitized_username}")

        return user

    except Exception as e:
        logger.error(f"Database error while fetching user '{username}': {str(e)}")
        raise InternalServerError("Failed to fetch user. Please try again later.")

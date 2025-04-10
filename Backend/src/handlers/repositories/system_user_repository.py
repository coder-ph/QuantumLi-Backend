from typing import Optional, List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from src.startup.database import db
from src.Models.systemusers import System_Users
from src.utils.logger import logger


class SystemUserRepository:
    def get_all_users(self) -> Optional[List[System_Users]]:
        try:
            users = System_Users.query.filter_by(is_deleted=False).all()
            logger.info(f"Fetched {len(users)} active users.")
            return users
        except SQLAlchemyError as e:
            logger.error(f"[get_all_users] DB error: {str(e)}", exc_info=True)
        except Exception as e:
            logger.error(f"[get_all_users] Unexpected error: {str(e)}", exc_info=True)
        return None

    def get_user_by_id(self, user_id: int) -> Optional[System_Users]:
        try:
            user = System_Users.query.filter_by(user_id=user_id, is_deleted=False).first()
            if user:
                logger.info(f"User {user_id} found.")
            else:
                logger.warning(f"User {user_id} not found or deleted.")
            return user
        except SQLAlchemyError as e:
            logger.error(f"[get_user_by_id] DB error for user {user_id}: {str(e)}", exc_info=True)
        except Exception as e:
            logger.error(f"[get_user_by_id] Unexpected error for user {user_id}: {str(e)}", exc_info=True)
        return None

    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[System_Users]:
        user = self.get_user_by_id(user_id)
        if not user:
            logger.warning(f"[update_user] Cannot update - user {user_id} not found.")
            return None

        try:
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    logger.warning(f"[update_user] Field '{key}' not found on user model. Skipping.")

            db.session.commit()
            logger.info(f"[update_user] User {user_id} updated successfully.")
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"[update_user] DB error while updating user {user_id}: {str(e)}", exc_info=True)
        except Exception as e:
            db.session.rollback()
            logger.error(f"[update_user] Unexpected error while updating user {user_id}: {str(e)}", exc_info=True)
        return None

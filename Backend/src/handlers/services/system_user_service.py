from typing import Optional, List, Dict, Any
from src.handlers.repositories.system_user_repository import SystemUserRepository
from src.Models.systemusers import System_Users
from src.utils.logger import logger


class SystemUserService:
    def __init__(self) -> None:
        self.user_repository = SystemUserRepository()

    def get_all_users(self) -> Optional[List[System_Users]]:
        try:
            users = self.user_repository.get_all_users()
            if not users:
                logger.warning("[get_all_users] No users found.")
                return None
            logger.info(f"[get_all_users] Retrieved {len(users)} users.")
            return users
        except Exception as e:
            logger.error(f"[get_all_users] Error: {str(e)}", exc_info=True)
            return None

    def get_user(self, user_id: int) -> Optional[System_Users]:
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                logger.warning(f"[get_user] User {user_id} not found.")
                return None
            logger.info(f"[get_user] User {user_id} retrieved successfully.")
            return user
        except Exception as e:
            logger.error(f"[get_user] Error fetching user {user_id}: {str(e)}", exc_info=True)
            return None

    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[System_Users]:
        try:
            user = self.user_repository.update_user(user_id, update_data)
            if not user:
                logger.warning(f"[update_user] Failed to update user {user_id}.")
                return None
            logger.info(f"[update_user] User {user_id} updated successfully.")
            return user
        except Exception as e:
            logger.error(f"[update_user] Error updating user {user_id}: {str(e)}", exc_info=True)
            return None

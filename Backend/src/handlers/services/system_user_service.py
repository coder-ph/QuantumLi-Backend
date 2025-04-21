from datetime import datetime, timedelta
import jwt
import os
from typing import Any, Dict, Optional
from uuid import UUID
from src.Models.systemusers import System_Users
from src.handlers.repositories.system_user_repository import SystemUserRepository
from src.utils.logger import logger
from src.utils.email_util import send_password_reset_email

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
JWT_ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_PREFIX = "reset_token:"

class SystemUserService:
    def __init__(self) -> None:
        self.user_repository = SystemUserRepository()

    def get_all_users(self) -> Optional[list[System_Users]]:
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

    def initiate_password_reset(self, email: str) -> bool:
        try:
            user = self.user_repository.get_user_by_email(email)
            if not user:
                logger.warning(f"[initiate_password_reset] User with email {email} not found.")
                return False

            reset_token = self.generate_reset_token(user)
            if not reset_token:
                logger.error(f"[initiate_password_reset] Failed to generate reset token for {email}.")
                return False

            send_password_reset_email(user.email, reset_token)
            logger.info(f"[initiate_password_reset] Password reset email sent to {email}.")
            return True
        except Exception as e:
            logger.error(f"[initiate_password_reset] Error for {email}: {str(e)}", exc_info=True)
            return False

    def generate_reset_token(self, user: System_Users) -> Optional[str]:
        try:
            payload = {
                'sub': str(user.user_id),
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
            }

            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            logger.info(f"[generate_reset_token] Token generated for user {user.email}")
            return token
        except Exception as e:
            logger.error(f"[generate_reset_token] Error: {str(e)}", exc_info=True)
            return None

    def verify_reset_token(self, token: str) -> Optional[System_Users]:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = UUID(payload.get("sub"))

            user = self.user_repository.get_user_by_id(user_id)
            return user
        except jwt.ExpiredSignatureError:
            logger.warning("[verify_reset_token] Token expired.")
        except jwt.InvalidTokenError as e:
            logger.warning(f"[verify_reset_token] Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"[verify_reset_token] Unexpected error: {str(e)}", exc_info=True)
        return None

    def reset_password(self, user_id: int, new_password_hash: str) -> bool:
        try:
            updated = self.user_repository.update_user(user_id, {"password_hash": new_password_hash})
            if updated:
                logger.info(f"[reset_password] Password updated for user {user_id}")
                return True
            else:
                logger.warning(f"[reset_password] Failed to update password for user {user_id}")
                return False
        except Exception as e:
            logger.error(f"[reset_password] Error resetting password: {str(e)}", exc_info=True)
            return False

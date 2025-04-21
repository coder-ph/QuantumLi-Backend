from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.handlers.services.system_user_service import SystemUserService
from src.schemas.system_user_schema import SystemUserSchema
from src.utils.logger import logger
from src.utils.decorators import roles_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import ValidationError
from datetime import datetime
from werkzeug.security import generate_password_hash

limiter = Limiter(key_func=get_remote_address)

user_service = SystemUserService()
user_schema = SystemUserSchema()
users_schema = SystemUserSchema(many=True)

@jwt_required()
@roles_required('admin')
@limiter.limit("5 per minute")
def get_all_users():
    try:
        users = user_service.get_all_users()
        if users:
            logger.info(f"[get_all_users] Retrieved {len(users)} users by admin.")
            users_data = users_schema.dump(users)
            return jsonify(users_data), 200
        logger.warning("[get_all_users] No users found.")
        return jsonify({"message": "No users found"}), 404
    except Exception as e:
        logger.error(f"[get_all_users] Error: {str(e)}", exc_info=True)
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@limiter.limit("5 per minute")
def update_user():
    current_user_id = get_jwt_identity()
    try:
        data = request.get_json()
        if not data:
            logger.warning(f"[update_user] Empty request body for user {current_user_id}.")
            return jsonify({"message": "No data provided"}), 400

        validated_data = user_schema.load(data, partial=True)

        user = user_service.update_user(current_user_id, validated_data)
        if user:
            logger.info(f"[update_user] User {current_user_id} updated successfully.")
            return user_schema.jsonify(user), 200

        logger.warning(f"[update_user] Update failed for user {current_user_id}.")
        return jsonify({"message": "Failed to update user"}), 400

    except ValidationError as ve:
        logger.warning(f"[update_user] Validation error for user {current_user_id}: {ve.messages}")
        return jsonify({"errors": ve.messages}), 422
    except Exception as e:
        logger.error(f"[update_user] Error updating user {current_user_id}: {str(e)}", exc_info=True)
        return jsonify({"message": "Internal server error"}), 500


@limiter.limit("5 per minute")
def request_password_reset():
    try:
        data = request.get_json()
        email = data.get('email', None)
        
        if not email:
            logger.warning("[request_password_reset] No email provided.")
            return jsonify({"message": "Email is required."}), 400
        
        result = user_service.initiate_password_reset(email)
        if result:
            logger.info(f"[request_password_reset] Password reset request initiated for {email}.")
            return jsonify({"message": "Password reset email sent successfully."}), 200
        
        logger.warning(f"[request_password_reset] No user found for email: {email}.")
        return jsonify({"message": "User with this email does not exist."}), 404

    except Exception as e:
        logger.error(f"[request_password_reset] Error: {str(e)}", exc_info=True)
        return jsonify({"message": "Internal server error"}), 500


@limiter.limit("5 per minute")
def reset_password():
    try:
        data = request.get_json()
        logger.info(f"[reset_password] Received data: {data}")
        reset_token = data.get('reset_token', None)
        new_password = data.get('new_password', None)
        confirm_password = data.get('confirm_password', None)

        if new_password != confirm_password:
            return jsonify({"message": "Passwords do not match."}), 400

        
        if not reset_token or not new_password:
            logger.warning("[reset_password] Missing reset token or new password.")
            return jsonify({"message": "Reset token and new password are required."}), 400
        
        if len(new_password) < 8:
            return jsonify({"message": "Password must be at least 8 characters long."}), 400
        
        user = user_service.verify_reset_token(reset_token)
        if not user:
            logger.warning("[reset_password] Invalid or expired reset token.")
            return jsonify({"message": "Invalid or expired reset token."}), 400
        
        hashed_password = generate_password_hash(new_password)
       
        result = user_service.reset_password(user.user_id, hashed_password)
        if result:
            logger.info("[reset_password] Password reset successfully.")
            return jsonify({"message": "Password has been reset successfully."}), 200
        
        logger.warning("[reset_password] Failed to reset password.")
        return jsonify({"message": "Failed to reset password."}), 400

    except Exception as e:
        logger.error(f"[reset_password] Error: {str(e)}", exc_info=True)
        return jsonify({"message": "Internal server error"}), 500

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.handlers.services.system_user_service import SystemUserService
from src.schemas.system_user_schema import SystemUserSchema
from src.utils.logger import logger
from src.utils.decorators import roles_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import ValidationError

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
            return users_schema.jsonify(users), 200
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

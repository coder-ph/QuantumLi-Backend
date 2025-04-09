from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from src.utils.logger import logger

def roles_required(required_role):
    """
    A decorator to check if the logged-in user has the required role.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                current_user = get_jwt_identity()
                user_role = current_user.get('role', None)
    
                if user_role != required_role:
                    logger.warning(f"Unauthorized access attempt by user {current_user.get('username')}.")
                    return jsonify({"message": "You do not have permission to access this resource."}), 403

                return fn(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in roles_required decorator: {str(e)}")
                return jsonify({"message": "An error occurred while verifying your role."}), 500

        return wrapper
    return decorator

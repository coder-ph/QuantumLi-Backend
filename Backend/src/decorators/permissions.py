from functools import wraps
from flask import request, jsonify
from flask_login import current_user
from src.utils.logger import logger

def role_required(allowed_roles):
    """
    Decorator to enforce role-based access control for Flask views.

    Args:
        allowed_roles (list): List of roles permitted to access the route.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_ip = request.remote_addr

            if not current_user.is_authenticated:
                logger.warning(f"Unauthorized access attempt from {user_ip}: User not authenticated")
                return jsonify({"message": "Authentication required"}), 401

            if not hasattr(current_user, 'role'):
                logger.error(f"Role attribute missing on user object ({current_user})")
                return jsonify({"message": "Role not defined for current user"}), 500

            if current_user.role not in allowed_roles:
                logger.warning(f"Access denied for user {current_user.email} ({user_ip}), role: {current_user.role}")
                return jsonify({
                    "message": f"Access denied. Your role '{current_user.role}' is not permitted for this resource."
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

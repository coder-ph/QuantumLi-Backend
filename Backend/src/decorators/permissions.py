from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from src.utils.logger import logger

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_ip = request.remote_addr

            try:
                verify_jwt_in_request()  
                jwt_data = get_jwt()     
            except Exception as e:
                logger.warning(f"Unauthorized access attempt from {user_ip}: {str(e)}")
                return jsonify({"message": "Authentication required"}), 401

            user_email = jwt_data.get('email')
            user_role = jwt_data.get('role')

            if not user_role:
                logger.error(f"Role claim missing in token for user {user_email} ({user_ip})")
                return jsonify({"message": "Role not provided in token"}), 403

            if user_role not in allowed_roles:
                logger.warning(f"Access denied for user {user_email} ({user_ip}), role: {user_role}")
                return jsonify({
                    "message": f"Access denied. Your role '{user_role}' is not permitted for this resource."
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

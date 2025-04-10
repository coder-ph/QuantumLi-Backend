from flask import Blueprint
from src.handlers.controllers.system_user_controller import get_all_users, update_user

system_user_bp = Blueprint('system_user_bp', __name__)

system_user_bp.add_url_rule('/system_users', 'get_all_users', get_all_users, methods=['GET'])
system_user_bp.add_url_rule('/system_users', 'update_user', update_user, methods=['PUT'])

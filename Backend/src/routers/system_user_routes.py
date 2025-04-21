from flask import Blueprint
from src.handlers.controllers.system_user_controller import get_all_users, update_user,reset_password, request_password_reset

system_user_bp = Blueprint('system_user_bp', __name__)

system_user_bp.add_url_rule('/system_users', 'get_all_users', get_all_users, methods=['GET'])
system_user_bp.add_url_rule('/system_users', 'update_user', update_user, methods=['PUT'])
system_user_bp.add_url_rule('/password-reset-request', 'password_reset_request', request_password_reset, methods=['POST'])
system_user_bp.add_url_rule('/password-reset', 'password_reset', reset_password, methods=['POST'])


{
  "reset_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjNGY2YTgwYS1kMjYxLTRhZmQtYjMyNi1iOGM2NmYzYmY3MjAiLCJlbWFpbCI6InBoZWxpeG90dHlAZ21haWwuY29tIiwiZXhwIjoxNzQ1MjQ2NTk3fQ.sCcAubU7wTiMIYN5tAVXrpaVTjs-gXsOxPkd-4rk5iM",
  "new_password": "NewSecurePass123!",
  "confirm_password": "NewSecurePass123!"
}
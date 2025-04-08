from flask import Blueprint
from src.handlers.controllers.auth_controller import login, logout, signup, verify_email


auth_bp = Blueprint('auth', __name__)


auth_bp.add_url_rule('/login', 'login', login, methods=['POST'])
auth_bp.add_url_rule('/logout', 'logout', logout, methods=['POST'])  
auth_bp.add_url_rule('/signup',   'signup',  signup,methods=['POST'])
auth_bp.add_url_rule('/verify-email', 'verify-email',  verify_email,methods=['GET'])

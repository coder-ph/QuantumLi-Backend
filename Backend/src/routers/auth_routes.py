from flask import Blueprint
from src.handlers.controllers.auth_controller import login, logout, signup, verify_email


auth_bp = Blueprint('auth', __name__)


auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/logout', methods=['POST'])(logout)
auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route('/verify-email', methods=['GET'])(verify_email)

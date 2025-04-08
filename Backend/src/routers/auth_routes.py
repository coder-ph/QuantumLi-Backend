from flask import Blueprint
from src.handlers.controllers.auth_controller import login
from src.handlers.controllers.auth_controller import logout  

auth_bp = Blueprint('auth', __name__)


auth_bp.add_url_rule('/login', 'login', login, methods=['POST'])
auth_bp.add_url_rule('/logout', 'logout', logout, methods=['POST'])  

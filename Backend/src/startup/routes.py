from flask import Blueprint
from src.handlers.controllers.auth_controller import login

auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/login', 'login', login, methods=['POST'])

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
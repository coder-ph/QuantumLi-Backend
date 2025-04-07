from flask import Blueprint
from src.routers.auth_routes import auth_bp


def register_routes(app):
     app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
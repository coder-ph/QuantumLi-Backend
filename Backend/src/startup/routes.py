from flask import Blueprint
from src.routers.auth_routes import auth_bp
from src.routers.product_routes import product_bp
from src.routers.system_user_routes import system_user_bp


def register_routes(app):
     app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
     app.register_blueprint(product_bp, url_prefix='/api/v1/product')
     app.register_blueprint(system_user_bp, url_prefix='api/v1/systUser')
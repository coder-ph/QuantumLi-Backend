from flask import Blueprint
from src.routers.auth_routes import auth_bp
from src.routers.product_routes import product_bp
from src.routers.system_user_routes import system_user_bp
from src.routers.billing_router import billing_bp
from src.routers.drivers_router import drivers_bp
from src.routers.incident_routes import incidents_bp
from src.routers.client_routes import client_bp
from src.routers.order_routes import orders_bp

def register_routes(app):
     app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
     app.register_blueprint(product_bp, url_prefix='/api/v1/product')
     app.register_blueprint(system_user_bp, url_prefix='/api/v1/systUser')
     app.register_blueprint(billing_bp, url_prefix='/api/v1/billing')
     app.register_blueprint(drivers_bp, url_prefix='/api/v1/drivers')
     app.register_blueprint(incidents_bp, url_prefix='/api/v1/incidents')
     app.register_blueprint(client_bp, url_prefix='/api/v1/clients')
     app.register_blueprint(orders_bp, url_prefix='/api/v1/orders')
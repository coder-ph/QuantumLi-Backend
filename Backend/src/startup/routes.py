from flask import Blueprint

from src.routers.auth_routes import auth_bp
from src.routers.product_routes import product_bp
from src.routers.system_user_routes import system_user_bp
from src.routers.billing_router import billing_bp
from src.routers.drivers_router import drivers_bp
from src.routers.incident_routes import incidents_bp
from src.routers.client_routes import client_bp
from src.routers.order_routes import orders_bp
from src.routers.order_response_routes import order_responses_bp
from src.routers.notification_routes import notification_bp
from src.routers.driver_assignment_routes import driver_assignment_bp
from src.routers.performance_metrics_routes import performance_metrics_bp
from src.routers.driver_performance_routes import driver_performance_bp


def register_routes(app):
     app.register_blueprint(auth_bp, url_prefix='/auth')
     app.register_blueprint(product_bp, url_prefix='/api/v1')
     app.register_blueprint(system_user_bp, url_prefix='/api/v1')
     app.register_blueprint(billing_bp, url_prefix='/api/v1')
     app.register_blueprint(drivers_bp, url_prefix='/api/v1')
     app.register_blueprint(incidents_bp, url_prefix='/api/v1')
     app.register_blueprint(client_bp, url_prefix='/api/v1')
     app.register_blueprint(orders_bp, url_prefix='/api/v1')
     app.register_blueprint(order_responses_bp, url_prefix='/api/v1')
     app.register_blueprint(notification_bp, url_prefix='/api/v1')
     app.register_blueprint(driver_assignment_bp, url_prefix='/api/v1/driver-assignment')
     app.register_blueprint(performance_metrics_bp, url_prefix='/api/v1/performance')
     app.register_blueprint(driver_performance_bp, url_prefix='/api')

from flask import Blueprint
from src.handlers.controllers.performance_metrics_controller import (
    get_deliveries_per_driver,
    get_average_delivery_time,
    get_order_acceptance_rejection,
    get_customer_ratings
)

performance_metrics_bp = Blueprint('performance_metrics_bp', __name__)


performance_metrics_bp.route('/deliveries-per-driver', methods=['GET'])(get_deliveries_per_driver)
performance_metrics_bp.route('/average-delivery-time', methods=['GET'])(get_average_delivery_time)
performance_metrics_bp.route('/order-acceptance-rejection', methods=['GET'])(get_order_acceptance_rejection)
performance_metrics_bp.route('/customer-ratings', methods=['GET'])(get_customer_ratings)

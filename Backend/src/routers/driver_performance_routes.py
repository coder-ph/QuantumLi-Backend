from flask import Blueprint
from src.handlers.controllers.performance_metrics_controller import get_deliveries_per_driver

driver_performance_bp = Blueprint('driver_performance_bp', __name__)

@driver_performance_bp.route('/driver-performance', methods=['GET'])
def driver_performance():
    return get_deliveries_per_driver()

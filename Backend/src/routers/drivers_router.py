from flask import Blueprint
from src.handlers.controllers.driver_controller import (
    create_driver_view,
    get_all_drivers_view,
    get_driver_view,
    update_driver_view,
    delete_driver_view
)

drivers_bp = Blueprint('drivers_bp', __name__)

drivers_bp.route('/drivers', methods=['POST'])(create_driver_view)
drivers_bp.route('/drivers', methods=['GET'])(get_all_drivers_view)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['GET'])(get_driver_view)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['PUT'])(update_driver_view)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['DELETE'])(delete_driver_view)

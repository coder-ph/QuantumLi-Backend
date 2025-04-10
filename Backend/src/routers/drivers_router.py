from flask import Blueprint
from src.handlers.controllers.driver_controller import (
    create_driver,
    get_all_drivers,
    get_driver,
    update_driver,
    delete_driver
)

drivers_bp = Blueprint('drivers_bp', __name__)

drivers_bp.route('/drivers', methods=['POST'])(create_driver)
drivers_bp.route('/drivers', methods=['GET'])(get_all_drivers)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['GET'])(get_driver)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['PUT'])(update_driver)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['DELETE'])(delete_driver)

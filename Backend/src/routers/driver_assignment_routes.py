from flask import Blueprint
from src.handlers.controllers.driver_assignment_controller import assign_driver_view

driver_assignment_bp = Blueprint('driver_assignment_bp', __name__)

driver_assignment_bp.route('/orders/<uuid:order_id>/assign-driver', methods=['POST'])(assign_driver_view)
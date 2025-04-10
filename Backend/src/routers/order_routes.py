from flask import Blueprint
from src.handlers.controllers.order_controller import (
    create_order_view,
    get_orders_view,
    get_order_view,
    update_order_view,
    assign_driver_view
)

orders_bp = Blueprint('orders_bp', __name__)

orders_bp.route('/orders', methods=['POST'])(create_order_view)
orders_bp.route('/orders', methods=['GET'])(get_orders_view)
orders_bp.route('/orders/<uuid:order_id>', methods=['GET'])(get_order_view)
orders_bp.route('/orders/<uuid:order_id>', methods=['PUT'])(update_order_view)
orders_bp.route('/orders/<uuid:order_id>/assign-driver', methods=['POST'])(assign_driver_view)

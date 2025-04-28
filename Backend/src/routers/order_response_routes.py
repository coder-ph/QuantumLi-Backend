from flask import Blueprint
from src.handlers.controllers.order_response_controller import (
    create_order_response_view,
    get_order_responses_view,
    get_order_response_view,
    update_order_response_view,
    delete_order_response_view
)

order_responses_bp = Blueprint('order_responses_bp', __name__)

order_responses_bp.route('/order-responses', methods=['POST'])(create_order_response_view)
order_responses_bp.route('/order-responses', methods=['GET'])(get_order_responses_view)
order_responses_bp.route('/order-responses/<uuid:response_id>', methods=['GET'])(get_order_response_view)
order_responses_bp.route('/order-responses/<uuid:response_id>', methods=['PUT'])(update_order_response_view)
order_responses_bp.route('/order-responses/<uuid:response_id>', methods=['DELETE'])(delete_order_response_view)
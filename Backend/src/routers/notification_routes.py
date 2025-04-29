from flask import Blueprint
from src.handlers.controllers.notification_controller import (
    create_notification_view,
    get_notification_response_view,
    record_notification_response_view
)

notification_bp = Blueprint('notification_bp', __name__)

notification_bp.route('/notifications', methods=['POST'])(create_notification_view)
notification_bp.route('/notifications/<uuid:notification_id>/response', methods=['GET'])(get_notification_response_view)
notification_bp.route('/notifications/<uuid:notification_id>/response', methods=['POST'])(record_notification_response_view)
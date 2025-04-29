from flask import jsonify, request
from src.handlers.services.notification_service import NotificationService
from src.utils.logger import logger

def create_notification_view():
    try:
        data = request.json
        recipient_id = data.get('recipient_id')
        message = data.get('message')
        type = data.get('type')
        related_entity = data.get('related_entity')
        related_id = data.get('related_id')
        buttons = data.get('buttons')
        email = data.get('email')

        if not recipient_id or not message or not type:
            return jsonify({"error": "Missing required fields"}), 400

        notification = NotificationService.create_notification(
            recipient_id=recipient_id,
            message=message,
            type=type,
            related_entity=related_entity,
            related_id=related_id,
            buttons=buttons,
            email=email
        )
        return jsonify({"message": "Notification created successfully", "notification_id": notification.notification_id}), 201
    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def get_notification_response_view(notification_id):
    try:
        response = NotificationService.get_response(notification_id)
        if response:
            return jsonify({"response": response}), 200
        return jsonify({"message": "No response found"}), 404
    except Exception as e:
        logger.error(f"Error fetching notification response: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def record_notification_response_view(notification_id):
    try:
        data = request.json
        driver_id = data.get('driver_id')
        order_id = data.get('order_id')
        status = data.get('status')
        reason = data.get('reason')

        if not driver_id or not order_id or not status:
            return jsonify({"error": "Missing required fields"}), 400

        success = NotificationService.record_response(
            notification_id=notification_id,
            driver_id=driver_id,
            order_id=order_id,
            status=status,
            reason=reason
        )
        if success:
            return jsonify({"message": "Response recorded successfully"}), 200
        return jsonify({"error": "Failed to record response"}), 500
    except Exception as e:
        logger.error(f"Error recording notification response: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
from src.Models.notification import Notifications
from src.Models.orderResponse import OrderResponse, ResponseStatus
from src.startup.database import db
from src.startup.socketio import socketio
from src.utils.logger import logger
from src.utils.email_util import send_email
from datetime import datetime
import uuid

class NotificationService:
    @staticmethod
    def create_notification(recipient_id, message, type, related_entity=None, related_id=None, buttons=None, email=None):
        """
        Create and send a notification to a recipient via Flask-SocketIO.
        If the recipient is inactive or SocketIO fails, fallback to email.

        Args:
            recipient_id (str): The ID of the recipient (e.g., driver or user).
            message (str): The notification message.
            type (str): The type of notification (e.g., "task_assignment").
            related_entity (str): The entity related to the notification (e.g., "order").
            related_id (str): The ID of the related entity.
            buttons (list): Optional list of buttons (e.g., ["Accept", "Reject"]).
            email (str): The recipient's email address for fallback.

        Returns:
            Notifications: The created notification object.
        """
        try:
            
            notification = Notifications(
                notification_id=str(uuid.uuid4()),
                recipient_id=recipient_id,
                message=message,
                type=type,
                status='unread',
                related_entity=related_entity,
                related_id=related_id,
                buttons=buttons,
                created_at=datetime.utcnow()
            )
            db.session.add(notification)
            db.session.commit()

           
            try:
                socketio.emit(
                    'notification',
                    {
                        'notification_id': notification.notification_id,
                        'message': message,
                        'type': type,
                        'related_entity': related_entity,
                        'related_id': related_id,
                        'buttons': buttons
                    },
                    room=recipient_id  
                )
                logger.info(f"Notification sent to recipient {recipient_id} via SocketIO.")
            except Exception as e:
                logger.warning(f"SocketIO notification failed for recipient {recipient_id}: {str(e)}")
                
                if email:
                    NotificationService._send_email_fallback(email, message, type, related_entity, related_id)
                else:
                    logger.error(f"No email provided for fallback notification to recipient {recipient_id}.")

            return notification
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}", exc_info=True)
            db.session.rollback()
            raise

    @staticmethod
    def _send_email_fallback(email, message, type, related_entity, related_id):
        """
        Send a fallback email notification.

        Args:
            email (str): The recipient's email address.
            message (str): The notification message.
            type (str): The type of notification.
            related_entity (str): The entity related to the notification.
            related_id (str): The ID of the related entity.
        """
        try:
            subject = f"Notification: {type.capitalize()}"
            body = f"""
            <h1>{type.capitalize()} Notification</h1>
            <p>{message}</p>
            <p>Related Entity: {related_entity}</p>
            <p>Related ID: {related_id}</p>
            """
            send_email(subject, body, email, is_html=True)
            logger.info(f"Fallback email sent to {email}.")
        except Exception as e:
            logger.error(f"Error sending fallback email to {email}: {str(e)}", exc_info=True)

    @staticmethod
    def get_response(notification_id):
        """
        Fetch the response to a notification.

        Args:
            notification_id (str): The ID of the notification.

        Returns:
            str: The response to the notification (e.g., "accepted", "rejected", or None if no response yet).
        """
        try:
            response = OrderResponse.query.filter_by(notification_id=notification_id).first()
            if response:
                return response.status.value  
            return None
        except Exception as e:
            logger.error(f"Error fetching response for notification {notification_id}: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def record_response(notification_id, driver_id, order_id, status, reason=None):
        """
        Record a driver's response to a notification.

        Args:
            notification_id (str): The ID of the notification.
            driver_id (str): The ID of the driver responding.
            order_id (str): The ID of the related order.
            status (str): The response status ("accepted" or "rejected").
            reason (str): Optional reason for rejection.

        Returns:
            bool: True if the response was recorded successfully, False otherwise.
        """
        try:
            response_status = ResponseStatus[status.upper()]
            order_response = OrderResponse(
                response_id=uuid.uuid4(),
                notification_id=notification_id,
                driver_id=driver_id,
                order_id=order_id,
                status=response_status,
                reason=reason,
                responded_at=datetime.utcnow()
            )
            db.session.add(order_response)
            db.session.commit()

           
            socketio.emit(
                'response',
                {
                    'notification_id': notification_id,
                    'driver_id': driver_id,
                    'order_id': order_id,
                    'status': status,
                    'reason': reason
                },
                room=driver_id  
            )
            logger.info(f"Response recorded for notification {notification_id}: {status}")
            return True
        except Exception as e:
            logger.error(f"Error recording response for notification {notification_id}: {str(e)}", exc_info=True)
            db.session.rollback()
            return False
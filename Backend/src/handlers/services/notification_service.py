from src.Models.notification import Notifications
from src.startup.database import db
from src.utils.logger import logger

class NotificationService:
    @staticmethod
    def create_notification(recipient_id, message, type, related_entity=None, related_id=None):
        try:
            notification = Notifications(
                recipient_id=recipient_id,
                message=message,
                type=type,
                status='unread',
                related_entity=related_entity,
                related_id=related_id
            )
            db.session.add(notification)
            db.session.commit()
            logger.info(f"Notification created for recipient {recipient_id}: {message}")
            return notification
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}", exc_info=True)
            db.session.rollback()
            raise
from src.Models.audit_logs import Audit_Logs
from src.startup.database import db
from datetime import datetime
from src.utils.logger import logger


def log_audit_event(user_id, action, ip, metadata=None, user_agent=None, endpoint=None):
    """
    Log an audit event to the database.

    Args:
        user_id (int or str): ID of the user performing the action.
        action (str): Description of the action performed (e.g., 'signup', 'login').
        ip (str): IP address of the requester.
        metadata (dict, optional): Any extra context or information to store.
        user_agent (str, optional): Info about the client browser/device.
        endpoint (str, optional): API endpoint triggered.
    """
    try:
        audit = Audit_Logs(
            user_id=user_id,
            action=action,
            ip_address=ip,
            user_agent=user_agent,
            endpoint=endpoint,
            metadata=metadata,
            timestamp=datetime.utcnow()
        )
        db.session.add(audit)
        db.session.commit()
        logger.info(f"Audit log created for user {user_id} | action: {action} | IP: {ip}")
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Failed to log audit event for user {user_id} | action: {action} | Reason: {str(e)}")

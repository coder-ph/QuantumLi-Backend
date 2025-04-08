from sqlalchemy import Enum
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from   src.startup.database import db
from datetime import datetime

class Notifications(db.Model):
    __tablename__ = 'notifications'

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    recipient_id = Column(UUID(as_uuid=True), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(Enum('sent', 'read', 'unread', 'failed', name='notification_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    read_at = Column(DateTime, nullable=True)
    related_entity = Column(String(100), nullable=True)
    related_id = Column(UUID(as_uuid=True), nullable=True)

    def __repr__(self):
        return f"<Notifications(notification_id={self.notification_id}, recipient_id={self.recipient_id}, type={self.type}, status={self.status})>"

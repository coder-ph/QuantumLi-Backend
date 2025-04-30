import uuid
import enum
import logging
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from src.startup.database import db
from src.utils.logger import logger

# Enums
class ResponseStatus(enum.Enum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class OrderResponse(db.Model):
    __tablename__ = 'order_responses'

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=False)
    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), nullable=False)
    status = Column(Enum(ResponseStatus), nullable=False)
    reason = Column(String(255), nullable=True)  # Nullable, only filled if rejected
    responded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship('Order', backref='responses', lazy=True)
    driver = relationship('Driver', backref='responses', lazy=True)

    def __repr__(self):
        return f"<OrderResponse(response_id={self.response_id}, driver_id={self.driver_id}, order_id={self.order_id}, status={self.status})>"

    @validates('status')
    def validate_status(self, key, value):
        if value not in ResponseStatus.__members__.values():
            logger.error(f"Invalid status: {value}")
            raise ValueError(f"Invalid status: {value}")
        logger.info(f"{key} validated successfully: {value}")
        return value

    @validates('reason')
    def validate_reason(self, key, value):
        if self.status == ResponseStatus.REJECTED and (not value or len(value.strip()) < 3):
            logger.error("Reason must be at least 3 characters when status is 'rejected'.")
            raise ValueError("Reason must be at least 3 characters when status is 'rejected'.")
        logger.info(f"{key} validated successfully: {value}")
        return value

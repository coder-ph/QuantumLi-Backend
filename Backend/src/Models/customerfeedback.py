from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from   app import db
from src.utils.logger import logger  # Assuming you have a logger utility

class Customer_Feedback(db.Model):
    __tablename__ = 'customer_feedback'

    # Unique feedback ID
    feedback_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Foreign Key referencing the Clients table
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.client_id'), nullable=False)

    # Foreign Key referencing the Order_Items table (not Orders)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey('order_items.order_item_id'), nullable=False)

    # Rating given by the client (1-5, or similar scale)
    rating = Column(Integer, nullable=False)

    # Additional comments provided by the client
    comments = Column(Text, nullable=True)

    # Date when the feedback was provided
    feedback_date = Column(Date, nullable=False, default=datetime.utcnow)

    # Whether follow-up is required after the feedback
    follow_up_required = Column(Boolean, default=False)

    # Current status of follow-up (open, completed, etc.)
    follow_up_status = Column(String(50), nullable=True)

    # Soft delete flag
    is_deleted = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(Date, nullable=False, default=datetime.utcnow)
    updated_at = Column(Date, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('rating')
    def validate_rating(self, key, value):
        """Ensure that rating is between 1 and 5"""
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return value

    def __repr__(self):
        return f"<Customer_Feedback(feedback_id={self.feedback_id}, client_id={self.client_id}, order_item_id={self.order_item_id}, rating={self.rating})>"

    def save(self):
        """Save the feedback entry"""
        db.session.add(self)
        db.session.commit()
        logger.info(f"Feedback created: {self.feedback_id}")

    def update(self):
        """Update the feedback entry"""
        db.session.commit()
        logger.info(f"Feedback updated: {self.feedback_id}")

    def delete(self):
        """Soft delete the feedback entry"""
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Feedback soft deleted: {self.feedback_id}")

    def restore(self):
        """Restore a soft-deleted feedback entry"""
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Feedback restored: {self.feedback_id}")

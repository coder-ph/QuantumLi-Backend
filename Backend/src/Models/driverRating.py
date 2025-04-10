from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from   src.startup.database import db
from sqlalchemy.orm import validates
from src.utils.logger import logger  

class Driver_Ratings(db.Model):
    __tablename__ = 'driver_ratings'

    rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), nullable=False)

    order_item_id = Column(UUID(as_uuid=True), ForeignKey('order_items.order_item_id'), nullable=False)
    rating = Column(Integer, nullable=False)

    comments = Column(Text, nullable=True)
    rating_date = Column(Date, nullable=False, default=datetime.utcnow)
    follow_up_required = Column(Boolean, default=False)
    follow_up_status = Column(Enum('open', 'resolved', 'pending', name='follow_up_status_enum'), nullable=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.client_id'), nullable=False)
    client = db.relationship('Client', back_populates='driver_ratings')
    is_deleted = Column(Boolean, default=False)
    created_at = Column(Date, nullable=False, default=datetime.utcnow)
    updated_at = Column(Date, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('rating')
    def validate_rating(self, key, value):
        
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return value

    def __repr__(self):
        return f"<Driver_Ratings(rating_id={self.rating_id}, driver_id={self.driver_id}, rating={self.rating}, order_item_id={self.order_item_id})>"

    def save(self):
       
        db.session.add(self)
        db.session.commit()
        logger.info(f"Driver rating created: {self.rating_id}")

    def update(self):
       
        db.session.commit()
        logger.info(f"Driver rating updated: {self.rating_id}")

    def delete(self):
      
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Driver rating soft deleted: {self.rating_id}")

    def restore(self):
      
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Driver rating restored: {self.rating_id}")

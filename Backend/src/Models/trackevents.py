import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from   src.startup.database import db
from src.Models.base_model import BaseModel
from src.utils.logger import logger
import re

class TrackingEvent(BaseModel):
    __tablename__ = 'tracking_events'

    tracking_event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey('shipments.shipment_id'), nullable=False)
    event_type = Column(String, nullable=False)
    event_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=False)
    gps_coordinates = Column(String, nullable=True)  
    event_description = Column(String, nullable=True)
    recorded_by = Column(String, nullable=False)  # user, driver, or system
    signature = Column(String, nullable=True) 
 


    deleted_at = Column(DateTime, nullable=True)

 
    shipment = relationship('Shipment', backref='tracking_events', lazy=True)
    location = relationship('Location', backref='tracking_events', lazy=True)

   
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TrackingEvent(id={self.tracking_event_id}, shipment_id={self.shipment_id}, event_type={self.event_type})>"

    @validates('gps_coordinates')
    def validate_gps_coordinates(self, key, value):
        """Ensure gps_coordinates is in a valid format (latitude, longitude)."""
        if value:
            pattern = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s?[-+]?((1[0-7]\d)|([1-9]?\d))(\.\d+)?$"
            if not re.match(pattern, value):
                logger.error(f"Invalid GPS coordinates: {value}")
                raise ValueError("Invalid GPS coordinates format.")
            logger.info(f"Valid GPS coordinates: {value}")
        return value

    def log_creation(self):
        """Log creation of a tracking event."""
        logger.info(f"TrackingEvent with ID {self.tracking_event_id} created at {self.created_at}.")

    def log_update(self):
        """Log updates to tracking event."""
        logger.info(f"TrackingEvent with ID {self.tracking_event_id} updated at {self.updated_at}.")

    
    def delete(self):
        """Mark this record as deleted (soft delete)."""
        self.deleted_at = datetime.utcnow()
        db.session.commit()
        logger.info(f"TrackingEvent with ID {self.tracking_event_id} marked as deleted at {self.deleted_at}.")
        
    @classmethod
    def query(cls):
        """Override the query to exclude soft-deleted records."""
        return db.session.query(cls).filter(cls.deleted_at == None)

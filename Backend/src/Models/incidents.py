from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Enum, Float, Text, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app import db
from src.utils.logger import logger  # Assuming you have a logger utility

class Incidents(db.Model):
    __tablename__ = 'incidents'

    incident_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    related_to = Column(Enum('shipment', 'order', name='related_to_enum'), nullable=False)

    # Foreign key to either the shipment or order, depending on the `related_to` field
    related_id = Column(UUID(as_uuid=True), nullable=False)
    incident_type = Column(Enum('damage', 'delay', 'loss', 'theft', name='incident_type_enum'), nullable=False)
    severity = Column(Enum('high', 'medium', 'low', name='severity_enum'), nullable=False)
    description = Column(Text, nullable=False)
    reported_by = Column(String(255), nullable=False)
    report_date = Column(Date, nullable=False, default=datetime.utcnow)
    resolution_status = Column(Enum('open', 'resolved', 'pending', name='resolution_status_enum'), nullable=False)
    resolution_details = Column(Text, nullable=True)
    compensation_amount = Column(Float, nullable=True)

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Incidents(incident_id={self.incident_id}, related_to={self.related_to}, incident_type={self.incident_type}, severity={self.severity})>"

    def save(self):
        """Save the incident entry"""
        db.session.add(self)
        db.session.commit()
        logger.info(f"Incident created: {self.incident_id}")

    def update(self):
        """Update the incident entry"""
        db.session.commit()
        logger.info(f"Incident updated: {self.incident_id}")

    def delete(self):
        """Soft delete the incident entry"""
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Incident soft deleted: {self.incident_id}")

    def restore(self):
        """Restore a soft-deleted incident entry"""
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Incident restored: {self.incident_id}")

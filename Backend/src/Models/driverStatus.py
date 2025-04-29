import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, ForeignKey,Boolean
from sqlalchemy.dialects.postgresql import UUID
from src.startup.database import db


class DriverStatus(db.Model):
    __tablename__ = 'driver_statuses'

    driver_status_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'),unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    reason = Column(String(200), nullable=True)
    # updated_at = Column(Date, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"<DriverStatus(driver_status_id={self.driver_status_id}, driver_id={self.driver_id}, is_active={self.is_active}, reason={self.reason}, updated_at={self.updated_at}>"
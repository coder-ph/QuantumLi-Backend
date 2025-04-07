import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Enum, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
from Backend.src.startup.database import db

class Location(db.Model):
    __tablename__ = 'locations'
    
    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_name = Column(String(100), nullable=False)
    location_type = Column(Enum('warehouse', 'hub', 'customer', 'other', name='location_type'), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=True)
    contact_phone = Column(String(15), nullable=True)
    operating_hours = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)

   
    __table_args__ = (
        Index('idx_location_city_country', 'city', 'country'),
        Index('idx_location_type', 'location_type'),
        UniqueConstraint('address', name='uq_location_address')
    )


    def __repr__(self):
        return f"<Location(location_id={self.location_id}, location_name={self.location_name}, city={self.city}, country={self.country})>"

from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Float, Date, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from   src.startup.database import db
from src.utils.logger import logger  

class Rates(db.Model):
    __tablename__ = 'rates'

    
    rate_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.client_id'), nullable=True)
    rate_name = Column(String(255), nullable=False)
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    service_type = Column(Enum('air', 'road', 'sea', 'rail', name='service_type_enum'), nullable=False)
    origin_zone = Column(String(255), nullable=False)
    destination_zone = Column(String(255), nullable=False)
    weight_break = Column(String(255), nullable=False)
    volume_break = Column(String(255), nullable=False)
    rate_per_unit = Column(Float, nullable=False)
    minimum_charge = Column(Float, nullable=False)
    accessorial_charges = Column(Float, nullable=True)

    # # Currency in which the rate is quoted (e.g., USD, EUR, KES)
    # currency = Column(String(3), nullable=False)


    is_deleted = Column(Boolean, default=False)


    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Rates(rate_id={self.rate_id}, rate_name={self.rate_name}, service_type={self.service_type}, origin_zone={self.origin_zone}, destination_zone={self.destination_zone})>"

    def save(self):
       
        db.session.add(self)
        db.session.commit()
        logger.info(f"Rate created: {self.rate_id}")

    def update(self):
       
        db.session.commit()
        logger.info(f"Rate updated: {self.rate_id}")

    def delete(self):
        
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Rate soft deleted: {self.rate_id}")

    def restore(self):
      
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Rate restored: {self.rate_id}")

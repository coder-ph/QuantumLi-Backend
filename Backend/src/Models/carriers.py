import uuid
import re
import logging
from sqlalchemy import Column, String, Float, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from   src.startup.database import db


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Carrier(db.Model):
    __tablename__ = 'carriers'

    carrier_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    carrier_name = Column(String(255), nullable=False)
    carrier_type = Column(String(50), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(50), nullable=False)
    account_number = Column(String(100), nullable=True)
    contract_details = Column(Text, nullable=True)
    service_levels = Column(Text, nullable=True)
    insurance_details = Column(Text, nullable=True)
    performance_rating = Column(Float, nullable=True)

    
    vehicles = relationship("Vehicle", back_populates="carrier", lazy=True)
    shipments = relationship("Shipment",back_populates ="carrier", lazy=True)
    
    __table_args__ = (
        CheckConstraint('performance_rating >= 0 AND performance_rating <= 5', name='check_performance_rating'),
    )

    def __repr__(self):
        return f"<Carrier(carrier_id={self.carrier_id}, carrier_name={self.carrier_name}, carrier_type={self.carrier_type})>"

    @staticmethod
    def validate_email(email):
        
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            logger.error(f"Invalid email format: {email}")
            raise ValueError(f"Invalid email format: {email}")
        logger.info(f"Valid email format: {email}")
        return email

    @staticmethod
    def validate_phone(phone):
        
        if phone.startswith('07'):
            if len(phone) != 10:
                logger.error(f"Phone number starting with '07' must be 10 digits: {phone}")
                raise ValueError(f"Phone number starting with '07' must be 10 digits: {phone}")
        elif phone.startswith('+254'):
            if len(phone) != 13:
                logger.error(f"Phone number starting with '+254' must be 13 characters: {phone}")
                raise ValueError(f"Phone number starting with '+254' must be 13 characters: {phone}")
        else:
            logger.error(f"Invalid phone number format: {phone}. It must start with '07' or '+254'.")
            raise ValueError(f"Invalid phone number format: {phone}. It must start with '07' or '+254'.")
        
        logger.info(f"Valid phone number: {phone}")
        return phone

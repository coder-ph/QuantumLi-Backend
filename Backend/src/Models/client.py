import uuid
import re
import logging
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from   src.startup.database import db
from src.Models.driverRating import Driver_Ratings
from sqlalchemy import UniqueConstraint


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Client(db.Model):
    __tablename__ = 'clients'
    
    client_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(14), nullable=False)  
    address = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)
    registration_number = Column(String(50), nullable=True)
    driver_ratings = db.relationship("Driver_Ratings", back_populates="client")
    account_status = Column(Enum('active', 'inactive', name='account_status'), default='active')
    credit_limit = Column(Float, nullable=True)
    payment_terms = Column(String(50), nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('email', name='uq_client_email'),
        UniqueConstraint('tax_id', name='uq_client_tax_id'),
        UniqueConstraint('registration_number', name='uq_client_registration_number'),
    )

    def __repr__(self):
        return f"<Client(client_id={self.client_id}, company_name={self.company_name}, email={self.email})>"

    @validates('email')
    def validate_email(self, key, email):
        """Validates email format."""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            logger.error(f"Invalid email format: {email}")
            raise ValueError(f"Invalid email format: {email}")
        logger.info(f"Valid email format: {email}")
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        """Validates phone number format."""
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

import uuid
import logging
from datetime import datetime
from src.Models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.startup.database import db
import re


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Driver(BaseModel):
    __tablename__ = 'drivers'
    
    driver_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    carrier_id = Column(UUID(as_uuid=True), ForeignKey('carriers.carrier_id'), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    license_number = Column(String(100), nullable=False, unique=True)
    license_type = Column(String(50), nullable=False)
    license_expiry = Column(Date, nullable=False)
    contact_phone = Column(String(15), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    address = Column(String(255), nullable=True)
    emergency_contact = Column(String(255), nullable=True)
    medical_certificate_expiry = Column(Date, nullable=False)
    training_certifications = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default='active')  

   
    carrier = relationship('Carrier', backref='drivers', lazy=True)
    # location = relationship('DriverLocation', backref='driver')
    documents = relationship('Document', back_populates='driver', lazy=True)

    responses = relationship('OrderResponse', backref='drivers', lazy=True)

    def __repr__(self):
        return f"<Driver(driver_id={self.driver_id}, first_name={self.first_name}, last_name={self.last_name})>"

    @staticmethod
    def validate_license_number(license_number):
        if len(license_number) > 100 or not license_number.isalnum():
            logger.error(f"Invalid license number: {license_number}. It should be alphanumeric and less than 100 characters.")
            raise ValueError("License number must be alphanumeric and no more than 100 characters.")
        logger.info(f"Valid license number: {license_number}")
        return license_number

    @staticmethod
    def validate_phone(phone):
        if not re.match(r"^(07\d{8}|(\+254)\d{9})$", phone):
            logger.error(f"Invalid phone number: {phone}. It should start with '07' or '+254' and be 13 characters long.")
            raise ValueError("Phone number must be 13 characters long and start with '07' or '+254'.")
        logger.info(f"Valid phone number: {phone}")
        return phone

    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            logger.error(f"Invalid email address: {email}. It must be a valid email format.")
            raise ValueError("Email must be a valid email address.")
        logger.info(f"Valid email address: {email}")
        return email

    @staticmethod
    def validate_expiry_date(expiry_date, field_name):
        # Convert string to datetime.date if expiry_date is a string
        if isinstance(expiry_date, str):
            try:
                expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()  # Assuming date format is 'YYYY-MM-DD'
            except ValueError:
                logger.error(f"Invalid {field_name}: {expiry_date}. The date format should be 'YYYY-MM-DD'.")
                raise ValueError(f"{field_name} must be in the format 'YYYY-MM-DD'.")
        
        # Now we can safely compare the expiry_date with today's date
        if expiry_date <= datetime.utcnow().date():
            logger.error(f"Invalid {field_name}: {expiry_date}. Expiry date must be in the future.")
            raise ValueError(f"{field_name} must be a future date.")
        
        logger.info(f"Valid {field_name}: {expiry_date}")
        return expiry_date

    def validate_driver(self):
        try:
            self.license_number = self.validate_license_number(self.license_number)
            self.contact_phone = self.validate_phone(self.contact_phone)
            self.email = self.validate_email(self.email)
            self.license_expiry = self.validate_expiry_date(self.license_expiry, "license_expiry")
            self.medical_certificate_expiry = self.validate_expiry_date(self.medical_certificate_expiry, "medical_certificate_expiry")
            # self.status = self.validate_status(self.status)
        except ValueError as e:
            logger.error(f"Validation failed: {str(e)}")
            raise e


    # @staticmethod
    # def validate_expiry_date(expiry_date, field_name):
       
    #     if expiry_date <= datetime.utcnow().date():
    #         logger.error(f"Invalid {field_name}: {expiry_date}. Expiry date must be in the future.")
    #         raise ValueError(f"{field_name} must be a future date.")
    #     logger.info(f"Valid {field_name}: {expiry_date}")
    #     return expiry_date
   
        
   
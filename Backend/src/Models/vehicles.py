import uuid
import logging
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from   src.startup.database import db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    vehicle_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    carrier_id = Column(UUID(as_uuid=True), ForeignKey('carriers.carrier_id'), nullable=True)
    registration_number = Column(String(100), nullable=False, unique=True)
    vehicle_type = Column(String(50), nullable=False) 
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    max_weight_capacity = Column(Float, nullable=False)  
    max_volume_capacity = Column(Float, nullable=False) 
    current_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=True)
    status = Column(String(50), nullable=False)  
    last_maintenance_date = Column(Date, nullable=True)
    next_maintenance_date = Column(Date, nullable=True)
    insurance_expiry = Column(Date, nullable=False)

    carrier = relationship('Carrier', back_populates='vehicles', lazy=True)
    current_location = relationship('Location', backref='vehicles', lazy=True)

    def __repr__(self):
        return f"<Vehicle(vehicle_id={self.vehicle_id}, registration_number={self.registration_number}, vehicle_type={self.vehicle_type})>"

    @staticmethod
    def validate_registration_number(registration_number):
        """Ensure the registration number is alphanumeric and not too long."""
        if len(registration_number) > 100 or not registration_number.isalnum():
            logger.error(f"Invalid registration number: {registration_number}. It should be alphanumeric and less than 100 characters.")
            raise ValueError("Registration number must be alphanumeric and no more than 100 characters.")
        logger.info(f"Valid registration number: {registration_number}")
        return registration_number

    @staticmethod
    def validate_capacity(capacity, field_name):
        """Ensure that capacities are positive numbers."""
        if capacity <= 0:
            logger.error(f"Invalid {field_name}: {capacity}. {field_name} must be a positive number.")
            raise ValueError(f"{field_name} must be a positive number.")
        logger.info(f"Valid {field_name}: {capacity}")
        return capacity

    @staticmethod
    def validate_year(year):
        """Ensure the year is within a reasonable range (e.g., 1900 to current year)."""
        current_year = 2025
        if year < 1900 or year > current_year:
            logger.error(f"Invalid year: {year}. Year must be between 1900 and {current_year}.")
            raise ValueError(f"Year must be between 1900 and {current_year}.")
        logger.info(f"Valid year: {year}")
        return year

    def validate_vehicle(self):
        """Validate the vehicle data."""
        try:
            self.registration_number = self.validate_registration_number(self.registration_number)
            self.max_weight_capacity = self.validate_capacity(self.max_weight_capacity, "max_weight_capacity")
            self.max_volume_capacity = self.validate_capacity(self.max_volume_capacity, "max_volume_capacity")
            self.year = self.validate_year(self.year)
        except ValueError as e:
            logger.error(f"Validation failed: {str(e)}")
            raise e

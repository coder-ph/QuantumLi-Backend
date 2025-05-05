import uuid
import logging
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from   src.startup.database import db
from sqlalchemy.orm import validates
from src.Models.client import Client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.client_id'), nullable=False)
    sku = Column(String(100), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True)
    weight = Column(Float, nullable=True)
    dimensions = Column(String(50), nullable=True)  
    unit_volume = Column(Float, nullable=True)
    hazardous = Column(Boolean, default=False)
    perishable = Column(Boolean, default=False)
    temperature_requirements = Column(String(100), nullable=True)
    handling_requirements = Column(String(200), nullable=True)
    customs_tariff_code = Column(String(100), nullable=True)
    value = Column(Float, nullable=True)

    client = relationship("Client", back_populates="products")

    __table_args__ = (
        UniqueConstraint('client_id', 'sku', name='uq_client_sku'),
    )

    @validates('weight')
    def validate_weight(self, key, weight):
        if weight is not None and weight <= 0:
            logger.error(f"Invalid weight: {weight}. Weight must be a positive number.")
            raise ValueError("Weight must be a positive number.")
        logger.info(f"Valid weight: {weight}")
        return weight

    @validates('value')
    def validate_value(self, key, value):
       
        if value is not None and value <= 0:
            logger.error(f"Invalid value: {value}. Value must be a positive number.")
            raise ValueError("Value must be a positive number.")
        logger.info(f"Valid value: {value}")
        return value

    @validates('dimensions')
    def validate_dimensions(self, key, dimensions):
        if dimensions and not self._is_valid_dimensions_format(dimensions):
            logger.error(f"Invalid dimensions: {dimensions}. Must be in 'LxWxH' format.")
            raise ValueError("Dimensions must be in the format 'LxWxH' where L, W, and H are numbers.")
        logger.info(f"Valid dimensions: {dimensions}")
        return dimensions

    def _is_valid_dimensions_format(self, dimensions):
        parts = dimensions.split('x')
        return len(parts) == 3 and all(part.isdigit() for part in parts)

    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name={self.name}, client_id={self.client_id})>"

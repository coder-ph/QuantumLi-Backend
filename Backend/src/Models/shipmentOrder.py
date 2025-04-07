import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from Backend.src.startup.database import db
from src.Models.base_model import BaseModel
from src.utils.logger import logger

class ShipmentOrder(BaseModel):
    __tablename__ = 'shipment_orders'

    shipment_order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey('shipments.shipment_id'), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=False)

    loading_sequence = Column(Integer, nullable=False)
    unloading_sequence = Column(Integer, nullable=False)

   
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    shipment = relationship('Shipment', backref='shipment_orders', lazy=True)
    order = relationship('Order', backref='shipment_orders', lazy=True)

    def __repr__(self):
        return f"<ShipmentOrder(id={self.shipment_order_id}, shipment_id={self.shipment_id}, order_id={self.order_id})>"

    
    @validates('loading_sequence', 'unloading_sequence')
    def validate_sequence(self, key, value):
        """Ensure loading and unloading sequence are positive integers."""
        if value < 0:
            logger.error(f"Validation failed for {key}: {value} is invalid (must be positive).")
            raise ValueError(f"{key.replace('_', ' ').title()} must be a positive integer.")
        logger.info(f"Validation passed for {key}: {value} is valid.")
        return value

    def log_creation(self):
        """Log creation of shipment order."""
        logger.info(f"ShipmentOrder with ID {self.shipment_order_id} created at {self.created_at}.")

    def log_update(self):
        """Log updates to shipment order."""
        logger.info(f"ShipmentOrder with ID {self.shipment_order_id} updated at {self.updated_at}.")

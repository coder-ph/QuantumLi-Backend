import uuid
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from   src.startup.database import db
from sqlalchemy.orm import validates
from src.utils.logger import logger


class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    inventory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.product_id'), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=False)
    quantity_on_hand = Column(Integer, nullable=False, default=0)
    quantity_allocated = Column(Integer, nullable=False, default=0)
    quantity_on_order = Column(Integer, nullable=False, default=0)
    last_stock_take_date = Column(Date, nullable=True)
    bin_location = Column(String(100), nullable=True)
    batch_number = Column(String(100), nullable=True)
    expiry_date = Column(Date, nullable=True)

    product = relationship("Product", backref="inventory")
    location = relationship("Location", backref="inventory")
    
    __table_args__ = (
        Index('idx_inventory_product_id', 'product_id'),
        Index('idx_inventory_location_id', 'location_id'),
    )

    def __repr__(self):
        return f"<Inventory(inventory_id={self.inventory_id}, product_id={self.product_id}, location_id={self.location_id})>"

    @validates('quantity_on_hand', 'quantity_allocated', 'quantity_on_order')
    def validate_non_negative(self, key, value):
    
        if value < 0:
            logger.error(f"{key} must be non-negative. Provided value: {value}")
            raise ValueError(f"{key} must be non-negative. Provided value: {value}")
        logger.info(f"Valid {key}: {value}")
        return value

    @validates('expiry_date')
    def validate_expiry_date(self, key, value):
     
        if value and value <= datetime.utcnow().date():
            logger.error(f"Expiry date must be in the future. Provided date: {value}")
            raise ValueError(f"Expiry date must be in the future. Provided date: {value}")
        logger.info(f"Valid expiry date: {value}")
        return value

    @validates('batch_number')
    def validate_batch_number(self, key, value):
        if value and len(value) < 5:
            logger.error(f"Batch number must be at least 5 characters. Provided batch number: {value}")
            raise ValueError(f"Batch number must be at least 5 characters. Provided batch number: {value}")
        logger.info(f"Valid batch number: {value}")
        return value

# src/Models/order_item.py

import uuid
import logging
from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from Backend.src.startup.database import db

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_weight = Column(Float, nullable=False)
    unit_volume = Column(Float, nullable=False)
    handling_instructions = Column(String(255), nullable=True)
    inventory_source_id = Column(UUID(as_uuid=True), ForeignKey('inventory.inventory_id'), nullable=True)

    
    order = relationship('Order', backref='order_items', lazy=True)
    product = relationship('Product', backref='order_items', lazy=True)
    inventory_source = relationship('Inventory', backref='order_items', lazy=True)

    def __repr__(self):
        return f"<OrderItem(id={self.order_item_id}, order_id={self.order_id}, product_id={self.product_id})>"

   

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            logger.error(f"Invalid quantity: {quantity}. Must be positive.")
            raise ValueError("Quantity must be a positive integer.")
        logger.info(f"Validated quantity: {quantity}")
        return quantity

    @validates('unit_weight')
    def validate_unit_weight(self, key, weight):
        if weight <= 0:
            logger.error(f"Invalid unit weight: {weight}. Must be positive.")
            raise ValueError("Unit weight must be a positive number.")
        logger.info(f"Validated unit_weight: {weight}")
        return weight

    @validates('unit_volume')
    def validate_unit_volume(self, key, volume):
        if volume <= 0:
            logger.error(f"Invalid unit volume: {volume}. Must be positive.")
            raise ValueError("Unit volume must be a positive number.")
        logger.info(f"Validated unit_volume: {volume}")
        return volume

import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from Backend.src.startup.database import db
import enum
from src.utils.logger import logger  # Import the logger

# Enum for Movement Types
class MovementType(enum.Enum):
    RECEIPT = 'receipt'
    SHIPMENT = 'shipment'
    TRANSFER = 'transfer'

class InventoryMovement(db.Model):
    __tablename__ = 'inventory_movements'

    movement_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.product_id'), nullable=False)
    from_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=False)
    to_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)  
    reference_id = Column(UUID(as_uuid=True), nullable=True)  # Reference to order, shipment,
    reference_type = Column(String, nullable=True)  # Type of reference: 'order', 'shipment',
    movement_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    recorded_by = Column(String, nullable=False)  # , user, system
    batch_number = Column(String, nullable=True)  # Batch number for product, if applicable
    expiry_date = Column(DateTime, nullable=True)  # Expiry date for perishable products
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)  # Soft delete flag

    # Relationships
    product = relationship('Product', backref='inventory_movements', lazy=True)
    from_location = relationship('Location', foreign_keys=[from_location_id], backref='inventory_movements_from', lazy=True)
    to_location = relationship('Location', foreign_keys=[to_location_id], backref='inventory_movements_to', lazy=True)

    def __repr__(self):
        return f"<InventoryMovement(id={self.movement_id}, quantity={self.quantity}, type={self.movement_type})>"

    def delete(self):
        """Soft delete functionality"""
        self.is_deleted = True
        db.session.commit()
        logger.info(f"InventoryMovement {self.movement_id} soft deleted.")

    def restore(self):
        """Restore soft-deleted entry"""
        self.is_deleted = False
        db.session.commit()
        logger.info(f"InventoryMovement {self.movement_id} restored.")

    def save(self):
        """Save a new inventory movement"""
        db.session.add(self)
        db.session.commit()
        logger.info(f"InventoryMovement {self.movement_id} created.")

    def update(self):
        """Update an existing inventory movement"""
        db.session.commit()
        logger.info(f"InventoryMovement {self.movement_id} updated.")

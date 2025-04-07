import uuid
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Backend.src.startup.database import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    inventory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.product_id', index=True), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id', index=True), nullable=False)
    quantity_on_hand = Column(Integer, nullable=False, default=0)
    quantity_allocated = Column(Integer, nullable=False, default=0)
    quantity_on_order = Column(Integer, nullable=False, default=0)
    last_stock_take_date = Column(Date, nullable=True)
    bin_location = Column(String(100), nullable=True)
    batch_number = Column(String(100), nullable=True)
    expiry_date = Column(Date, nullable=True)

  
    product = relationship("Product", backref="inventory")
    location = relationship("Location", backref="inventory")

    def __repr__(self):
        return f"<Inventory(inventory_id={self.inventory_id}, product_id={self.product_id}, location_id={self.location_id})>"
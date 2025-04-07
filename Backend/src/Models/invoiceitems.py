from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app import db
from src.utils.logger import logger  # Assuming you have a logger in your utilities

class InvoiceItems(db.Model):
    __tablename__ = 'invoice_items'

    # Unique ID for each invoice item (UUID format)
    invoice_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Foreign key to the Billing table
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('billing.invoice_id'), nullable=False)

    # Description of the item being billed
    item_description = Column(String(255), nullable=False)

    # Type of service related to the item (e.g., shipment, storage)
    related_to = Column(Enum('shipment', 'storage', 'handling', 'other', name='invoice_item_related_to'), nullable=False)

    # Reference to the specific shipment or storage related to this item (e.g., shipment_id, storage_id)
    related_id = Column(UUID(as_uuid=True), nullable=False)

    # Quantity of the item
    quantity = Column(Float, nullable=False)

    # Unit price of the item
    unit_price = Column(Float, nullable=False)

    # Total price for this item (calculated as quantity * unit_price)
    total_price = Column(Float, nullable=False)

    # Tax rate applied to the item
    tax_rate = Column(Float, nullable=False)

    # Soft delete flag
    is_deleted = Column(Boolean, default=False)

    # Timestamp columns
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship back to the Billing table (to fetch the associated invoice)
    billing = relationship("Billing", backref="invoice_items")

    def __repr__(self):
        return f"<InvoiceItems(invoice_item_id={self.invoice_item_id}, invoice_id={self.invoice_id}, item_description={self.item_description}, total_price={self.total_price})>"

    def save(self):
        """Save the invoice item record"""
        db.session.add(self)
        db.session.commit()
        logger.info(f"Invoice item created: {self.invoice_item_id}")

    def update(self):
        """Update the invoice item record"""
        db.session.commit()
        logger.info(f"Invoice item updated: {self.invoice_item_id}")

    def delete(self):
        """Soft delete the invoice item record"""
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Invoice item soft deleted: {self.invoice_item_id}")

    def restore(self):
        """Restore soft-deleted invoice item record"""
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Invoice item restored: {self.invoice_item_id}")

    def calculate_total_price(self):
        """Calculate the total price for the item (quantity * unit price)"""
        self.total_price = self.quantity * self.unit_price
        return self.total_price

    def calculate_tax_amount(self):
        """Calculate the tax amount for the item (total_price * tax_rate)"""
        return self.total_price * self.tax_rate / 100

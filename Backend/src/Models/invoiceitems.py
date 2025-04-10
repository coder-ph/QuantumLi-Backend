from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from   src.startup.database import db
from src.utils.logger import logger  

class InvoiceItems(db.Model):
    __tablename__ = 'invoice_items'

    invoice_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('billing.invoice_id'), nullable=False)
    item_description = Column(String(255), nullable=False)
    related_to = Column(Enum('shipment', 'storage', 'handling', 'other', name='invoice_item_related_to'), nullable=False)
    related_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    tax_rate = Column(Float, nullable=False)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    billing = relationship("Billing", backref="invoice_items")

    def __repr__(self):
        return f"<InvoiceItems(invoice_item_id={self.invoice_item_id}, invoice_id={self.invoice_id}, item_description={self.item_description}, total_price={self.total_price})>"

    def save(self):
      
        db.session.add(self)
        db.session.commit()
        logger.info(f"Invoice item created: {self.invoice_item_id}")

    def update(self):
        
        db.session.commit()
        logger.info(f"Invoice item updated: {self.invoice_item_id}")

    def delete(self):
        
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Invoice item soft deleted: {self.invoice_item_id}")

    def restore(self):
        
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Invoice item restored: {self.invoice_item_id}")

    def calculate_total_price(self):
        
        self.total_price = self.quantity * self.unit_price
        return self.total_price

    def calculate_tax_amount(self):
       
        return self.total_price * self.tax_rate / 100

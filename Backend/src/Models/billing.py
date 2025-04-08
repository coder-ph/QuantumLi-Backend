from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.Models.client import Client
from   src.startup.database import db
from src.utils.logger import logger  # Assuming you have a logger in your utilities

class Billing(db.Model):
    __tablename__ = 'billing'

    invoice_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.client_id'), nullable=False)
    invoice_date = Column(Date, nullable=False, default=datetime.utcnow)
    due_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)

    status = Column(Enum('draft', 'paid', 'overdue', name='invoice_status'), nullable=False, default='draft')
    payment_date = Column(Date, nullable=True)
    payment_method = Column(String(50), nullable=True)  #  "Mpesa", "Credit Card", etc.

    reference_numbers = Column(String(100), nullable=True)
    notes = Column(String(255), nullable=True)

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

  
    client = relationship("Client", backref="billing_invoices")

    def __repr__(self):
        return f"<Billing(invoice_id={self.invoice_id}, client_id={self.client_id}, total_amount={self.total_amount}, status={self.status})>"

    def save(self):
        """Save the billing record"""
        db.session.add(self)
        db.session.commit()
        logger.info(f"Billing record created: {self.invoice_id}")

    def update(self):
        """Update the billing record"""
        db.session.commit()
        logger.info(f"Billing record updated: {self.invoice_id}")

    def delete(self):
        """Soft delete the billing record"""
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Billing record soft deleted: {self.invoice_id}")

    def restore(self):
        """Restore soft-deleted billing record"""
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Billing record restored: {self.invoice_id}")

    def is_overdue(self):
        """Check if the billing is overdue"""
        return self.due_date < datetime.utcnow().date() and self.status != 'paid'

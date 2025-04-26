import uuid
import enum
import logging
from datetime import date
from sqlalchemy import Column, String, Date, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from   src.startup.database import db
from src.utils.logger import logger

# Enums
class OrderStatus(enum.Enum):
    DRAFT = 'draft'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in progress'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

class BillingType(enum.Enum):
    PREPAID = 'prepaid'
    COLLECT = 'collect'
    THIRD_PARTY = 'third party'

class PaymentStatus(enum.Enum):
    PAID = 'paid'
    UNPAID = 'unpaid'
    PENDING = 'pending'

class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.client_id'), nullable=False)
    order_reference = Column(String(100), nullable=False, unique=True)
    order_date = Column(Date, nullable=False)
    requested_pickup_date = Column(Date, nullable=False)
    requested_delivery_date = Column(Date, nullable=False)
    priority = Column(String(50), nullable=False)
    special_instructions = Column(String(255), nullable=True)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.DRAFT)
    billing_type = Column(Enum(BillingType), nullable=False, default=BillingType.PREPAID)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    total_weight = Column(Float, nullable=False)
    total_volume = Column(Float, nullable=False)
    declared_value = Column(Float, nullable=False)
    required_documents = Column(String(255), nullable=True)

    client = relationship('Client', backref='orders', lazy=True)

    responses = relationship('OrderResponse', backref= 'orders', lazy=True)

    def __repr__(self):
        return f"<Order(order_id={self.order_id}, order_reference={self.order_reference}, client_id={self.client_id})>"


    @validates('total_weight', 'total_volume', 'declared_value')
    def validate_positive_values(self, key, value):
        if value <= 0:
            logger.error(f"{key} must be a positive number. Got: {value}")
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be a positive number.")
        logger.info(f"{key} validated successfully: {value}")
        return value

    @validates('order_date', 'requested_pickup_date', 'requested_delivery_date')
    def validate_dates(self, key, value):
        if not isinstance(value, date):
            logger.error(f"{key} must be a valid date object. Got: {value}")
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be a valid date.")
        logger.info(f"{key} validated successfully: {value}")
        return value

    @validates('order_reference')
    def validate_order_reference(self, key, value):
        if not value or len(value.strip()) < 3:
            logger.error("Order reference must be at least 3 characters.")
            raise ValueError("Order reference must be at least 3 characters.")
        logger.info(f"{key} validated successfully: {value}")
        return value

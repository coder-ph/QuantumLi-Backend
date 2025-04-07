import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from src.database import db
from src.Models.enums import ShipmentStatusEnum, ShippingMethodEnum
from src.Models.base_model import BaseModel
from src.utils.logger import logger

class Shipment(BaseModel):
    __tablename__ = 'shipments'

    shipment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_reference = Column(String(50), nullable=False, unique=True)

    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=True)
    carrier_id = Column(UUID(as_uuid=True), ForeignKey('carriers.carrier_id'), nullable=True)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey('vehicles.vehicle_id'), nullable=True)
    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), nullable=True)

    origin_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=False)
    destination_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=False)

    planned_departure = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    planned_arrival = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)

    status = Column(SqlEnum(ShipmentStatusEnum), nullable=False, default=ShipmentStatusEnum.PLANNED)
    shipping_method = Column(SqlEnum(ShippingMethodEnum), nullable=True)

    tracking_number = Column(String(100), nullable=True, unique=True)
    total_weight = Column(Float, nullable=True)
    total_volume = Column(Float, nullable=True)
    bill_of_lading_number = Column(String(100), nullable=True)

    shipping_cost = Column(Float, nullable=True)
    fuel_surcharge = Column(Float, nullable=True)
    accessorial_charges = Column(Float, nullable=True)

    temperature_monitoring = Column(Boolean, default=False)
    seal_number = Column(String(100), nullable=True)

    # Relationships
    carrier = relationship('Carrier', backref='shipments', lazy=True)
    vehicle = relationship('Vehicle', backref='shipments', lazy=True)
    driver = relationship('Driver', backref='shipments', lazy=True)
    origin_location = relationship('Location', foreign_keys=[origin_location_id], backref='origin_shipments', lazy=True)
    destination_location = relationship('Location', foreign_keys=[destination_location_id], backref='destination_shipments', lazy=True)
    order = relationship('Order', backref='shipments', lazy=True)

    def __repr__(self):
        return f"<Shipment(shipment_id={self.shipment_id}, reference={self.shipment_reference}, status={self.status.value})>"

    # Validations
    @validates('total_weight', 'total_volume', 'shipping_cost', 'fuel_surcharge', 'accessorial_charges')
    def validate_positive_numbers(self, key, value):
        if value is not None and value < 0:
            logger.error(f"Validation failed for {key}: {value} is invalid.")
            raise ValueError(f"{key.replace('_', ' ').title()} must be a positive number.")
        logger.info(f"Validation passed for {key}: {value} is valid.")
        return value

    @validates('shipment_reference')
    def validate_reference(self, key, value):
        if not value or len(value.strip()) < 3:
            logger.error(f"Validation failed for shipment_reference: {value} is too short.")
            raise ValueError("Shipment reference must be at least 3 characters long.")
        logger.info(f"Validation passed for shipment_reference: {value} is valid.")
        return value

import os
from datetime import datetime, timedelta
from src.startup.database import db
from src.Models.systemusers import System_Users
from src.Models.drivers import Driver
from src.Models.orders import Order, OrderStatus, BillingType, PaymentStatus
from src.Models.locations import Location
from src.Models.driverSchedule import DriverSchedule
from src.Models.billing import Billing
from src.Models.product import Product
from src.Models.inventory import Inventory
from src.Models.shipment import Shipment, ShipmentStatusEnum, ShippingMethodEnum
from src.Models.carriers import Carrier
from src.Models.orderItem import OrderItem
from src.Models.invoiceitems import InvoiceItems
from src.Models.trackevents import TrackingEvent
from src.Models.warehouseOperations import WarehouseOperation, OperationStatus
from src.Models.client import Client
from src.Models.rates import Rates
from src.Models.thirdparty import ThirdPartyService
from src.Models.incidents import Incidents
from src.utils.logger import logger


def seed_admin_user():
    admin_user = System_Users.query.filter_by(email="admin@example.com").first()
    if not admin_user:
        admin_user = System_Users(
            username="admin",
            email="admin@example.com",
            password_hash="hashed_password",  
            role="admin",
            phone="+254700000000",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(admin_user)
        logger.info("Admin user seeded successfully.")
    else:
        logger.info("Admin user already exists.")


def seed_driver_schedule():
    driver = Driver.query.filter_by(email="driver1@example.com").first()
    if driver:
        schedule = DriverSchedule.query.filter_by(driver_id=driver.driver_id).first()
        if not schedule:
            weekly_schedule = {
                "monday": {"work": True, "start": "08:00", "end": "17:00"},
                "tuesday": {"work": True, "start": "08:00", "end": "17:00"},
                "wednesday": {"work": True, "start": "08:00", "end": "17:00"},
                "thursday": {"work": True, "start": "08:00", "end": "17:00"},
                "friday": {"work": True, "start": "08:00", "end": "17:00"},
                "saturday": {"work": False, "start": None, "end": None},
                "sunday": {"work": False, "start": None, "end": None}
            }
            schedule = DriverSchedule(
                driver_id=driver.driver_id,
                weekly_schedule=weekly_schedule
            )
            db.session.add(schedule)
            db.session.commit()
            logger.info("Driver schedule seeded successfully.")
    else:
        logger.warning("Cannot create driver schedule - driver not found.")


def seed_drivers():
    driver = Driver.query.filter_by(email="driver1@example.com").first()
    if not driver:
        driver = Driver(
            first_name="John",
            last_name="Doe",
            email="driver1@example.com",
            license_number="ABC12345",
            license_expiry=datetime.utcnow() + timedelta(days=365),
            license_type="Class A",
            contact_phone="+254700000000",
            medical_certificate_expiry=datetime.utcnow() + timedelta(days=365),
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(driver)
        db.session.commit()  # Needed to generate driver_id
        logger.info("Driver seeded successfully.")
    else:
        logger.info("Driver already exists.")
    seed_driver_schedule()


def seed_clients():
    try:
        client = Client.query.filter_by(email="client1@example.com").first()
        if not client:
            client = Client(
                company_name="Example Company",
                contact_person="Jane Doe",
                email="client1@example.com",
                phone="+254700123456",
                address="123 Main Street, Nairobi, Kenya",
                tax_id="123456789",
                registration_number="REG12345",
                account_status="active",
                credit_limit=10000.0,
                payment_terms="Net 30",
            )
            db.session.add(client)
            logger.info("Client seeded successfully.")
        else:
            logger.info("Client already exists.")
    except Exception as e:
        logger.error(f"Error seeding client: {e}")


def seed_locations():
    location = Location.query.filter_by(location_name="Warehouse A").first()
    if not location:
        location = Location(
            location_name="Warehouse A",
            location_type="warehouse",
            address="123 Main Street",
            city="Nairobi",
            country="Kenya",
            contact_person="Jane Doe",
            contact_phone="+254700123456",
            is_active=True,
        )
        db.session.add(location)
        logger.info("Location seeded successfully.")
    else:
        logger.info("Location already exists.")


def seed_orders():
    order = Order.query.filter_by(order_reference="ORD001").first()
    if not order:
        client = Client.query.filter_by(email="client1@example.com").first()
        if not client:
            logger.warning("Client for order not found.")
            return
        order = Order(
            client_id=client.client_id,
            order_reference="ORD001",
            order_date=datetime.utcnow(),
            requested_pickup_date=datetime.utcnow() + timedelta(days=1),
            requested_delivery_date=datetime.utcnow() + timedelta(days=3),
            priority="high",
            special_instructions="Handle with care",
            status=OrderStatus.DRAFT,
            billing_type=BillingType.PREPAID,
            payment_status=PaymentStatus.PENDING,
            total_weight=100.0,
            total_volume=1.0,
            declared_value=1000.0,
            # created_at=datetime.utcnow(),
            # updated_at=datetime.utcnow()
        )
        db.session.add(order)
        logger.info("Order seeded successfully.")
    else:
        logger.info("Order already exists.")


def seed_products():
    product = Product.query.filter_by(sku="PROD001").first()
    if not product:
        client = Client.query.filter_by(email="client1@example.com").first()
        if not client:
            logger.warning("Client for product not found.")
            return
        product = Product(
            client_id=client.client_id,
            sku="PROD001",
            name="Sample Product",
            description="This is a sample product.",
            category="General",
            weight=10.0,
            dimensions="10x10x10",
            unit_volume=1.0,
            hazardous=False,
            perishable=False,
            value=100.0,
        )
        db.session.add(product)
        logger.info("Product seeded successfully.")
    else:
        logger.info("Product already exists.")


def main():
    logger.info("Starting database seeding...")
    seed_admin_user()
    seed_drivers()
    seed_clients()
    seed_locations()
    seed_orders()
    seed_products()
    db.session.commit()
    logger.info("Database seeding completed successfully.")


if __name__ == "__main__":
    from app import app
    with app.app_context():
        main()

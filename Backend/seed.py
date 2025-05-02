import uuid
from datetime import datetime, timedelta
from src.startup.database import db
from src.Models.client import Client
from src.Models.drivers import Driver
from src.Models.orders import Order, OrderStatus, BillingType, PaymentStatus
from src.Models.locations import Location
from src.Models.product import Product
from src.Models.systemusers import System_Users
from src.Models.driverSchedule import DriverSchedule
from src.Models.inventory import Inventory
from src.Models.billing import Billing
from src.utils.logger import logger
from app import app

def seed_data():
    with app.app_context():
        try:
            # Clear existing data
            db.session.query(Client).delete()
            db.session.query(Driver).delete()
            db.session.query(Order).delete()
            db.session.query(Location).delete()
            db.session.query(Product).delete()
            db.session.query(System_Users).delete()
            db.session.query(DriverSchedule).delete()
            db.session.query(Inventory).delete()
            db.session.query(Billing).delete()

            # Seed Clients
            client1 = Client(
                client_id=uuid.uuid4(),
                company_name="Quantum Logistics",
                contact_person="John Doe",
                email="john.doe@example.com",
                phone="+1234567890",
                address="123 Main St, Cityville",
                tax_id="TAX12345",
                registration_number="REG12345",
                account_status="active",
                credit_limit=10000.0,
                payment_terms="Net 30",
                date_created=datetime.utcnow(),
                last_updated=datetime.utcnow()
            )
            db.session.add(client1)

            # Seed Drivers
            driver1 = Driver(
                driver_id=uuid.uuid4(),
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                contact_phone="+9876543210",
                license_number="LIC12345",
                license_expiry=datetime.utcnow() + timedelta(days=365),
                medical_certificate_expiry=datetime.utcnow() + timedelta(days=365),
                status="active"
            )
            db.session.add(driver1)

            # Seed Orders
            order1 = Order(
                order_id=uuid.uuid4(),
                client_id=client1.client_id,
                order_reference="ORD12345",
                order_date=datetime.utcnow().date(),
                requested_pickup_date=datetime.utcnow().date() + timedelta(days=1),
                requested_delivery_date=datetime.utcnow().date() + timedelta(days=5),
                priority="high",
                special_instructions="Handle with care",
                status=OrderStatus.CONFIRMED,
                billing_type=BillingType.PREPAID,
                payment_status=PaymentStatus.PENDING,
                total_weight=100.0,
                total_volume=50.0,
                declared_value=5000.0,
                required_documents="Invoice, Packing List"
            )
            db.session.add(order1)

            # Seed Locations
            location1 = Location(
                location_id=uuid.uuid4(),
                location_name="Warehouse A",
                location_type="warehouse",
                address="456 Warehouse Rd, Cityville",
                city="Cityville",
                country="Countryland",
                contact_person="Alice Johnson",
                contact_phone="+1122334455",
                latitude=12.3456,
                longitude=78.9101
            )
            db.session.add(location1)

            # Seed Products
            product1 = Product(
                product_id=uuid.uuid4(),
                client_id=client1.client_id,
                sku="SKU12345",
                name="Product A",
                description="Description of Product A",
                category="Category A",
                weight=10.0,
                dimensions="10x20x30",
                hazardous=False,
                perishable=False
            )
            db.session.add(product1)

            # Seed System Users
            user1 = System_Users(
                user_id=uuid.uuid4(),
                username="admin",
                password_hash="hashed_password",
                email="admin@example.com",
                phone="+1234567890",
                role="admin",
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(user1)

            # Commit all changes
            db.session.commit()
            logger.info("Database seeded successfully.")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error seeding database: {str(e)}")
            raise

if __name__ == "__main__":
    seed_data()
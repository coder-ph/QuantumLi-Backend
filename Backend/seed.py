import os
from datetime import datetime, timedelta, timezone
from uuid import UUID
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
from src.Models.vehicles import Vehicle
from src.Models.employee import Employee
from src.utils.logger import logger

from faker import Faker #type: ignore
from random import randint, choice, uniform
import json
import uuid

fake = Faker()


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
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(admin_user)
        logger.info("Admin user seeded successfully.")
    else:
        logger.info("Admin user already exists.")
 

def seed_driver_schedule():

    drivers = Driver.query.all()

    def random_time_between(start="06:00", end="18:00"):
        start_dt = datetime.strptime(start, "%H:%M")
        end_dt = datetime.strptime(end, "%H:%M")
        delta = end_dt - start_dt
        random_minutes = fake.random_int(min=0, max=int(delta.total_seconds() // 60))
        random_time = (start_dt + timedelta(minutes=random_minutes)).strftime("%H:%M")
        return random_time

    for driver in drivers:
        try:
            if DriverSchedule.query.filter_by(driver_id=driver.driver_id).first():
                logger.info(f"Schedule already exists for driver_id={driver.driver_id}")
                continue

            weekly_schedule = {
                "monday": {"work": choice([True,False]), "start": f"{random_time_between("06:00", "10:00")}", "end": f"{random_time_between("15:00", "20:00")}"},
                "tuesday": {"work": choice([True,False]), "start": f"{random_time_between("06:00", "10:00")}", "end": f"{random_time_between("15:00", "20:00")}"},
                "wednesday": {"work": choice([True,False]), "start":f"{random_time_between("06:00", "10:00")}", "end": f"{random_time_between("15:00", "20:00")}"},
                "thursday": {"work": choice([True,False]), "start": f"{random_time_between("06:00", "10:00")}", "end": f"{random_time_between("15:00", "20:00")}"},
                "friday": {"work": choice([True,False]), "start": f"{random_time_between("06:00", "10:00")}", "end": f"{random_time_between("15:00", "20:00")}"},
                "saturday": {"work": choice([True,False]), "start": None, "end": None},
                "sunday": {"work": choice([True,False]), "start": None, "end": None}
            }
            schedule = DriverSchedule(
                driver_id=driver.driver_id,
                weekly_schedule=weekly_schedule
            )
            db.session.add(schedule)
            db.session.commit()
            logger.info("Driver schedule seeded successfully.")
        
        except:
            weekly_schedule=json.dumps(weekly_schedule)
            logger.warning("Cannot create driver schedule.")

    # driver = Driver.query.filter_by(email="driver1@example.com").first()
    # if driver:
    #     schedule = DriverSchedule.query.filter_by(driver_id=driver.driver_id).first()
    #     if not schedule:
            
    # else:
def seed_carriers():
    for i in range(1, 11): 
        email = fake.unique.company_email()
        
        try:
            carrier = Carrier(
                carrier_id=uuid.uuid4(),
                carrier_name=fake.company(),
                carrier_type=choice(['Logistics', 'Freight', 'Courier', 'Trucking', 'Air Cargo']),
                contact_person=fake.name(),
                email=email,
                phone=fake.phone_number(),
                account_number=fake.bban(), 
                contract_details=fake.text(max_nb_chars=200),
                service_levels=choice([
                    "Standard, Express, Overnight",
                    "Basic, Premium, Priority",
                    "Ground, Air, International"
                ]),
                insurance_details=fake.text(max_nb_chars=150),
                performance_rating=round(uniform(3.0, 5.0), 2)
            )
            
            db.session.add(carrier)
            db.session.commit()  
            
            logger.info(f"Carrier seeded successfully.")
        
        except Exception as e:
            logger.error(f"Carrier seeding failed for: {e}")
            db.session.rollback() 
    
    logger.info("Carriers seeding process completed.")


def seed_drivers():
    for i in range(1, 21):  
        email = f"{fake.email()}"
        driver = Driver.query.filter_by(email=email).first()
        carriers = Carrier.query.all()
        if not driver:
            driver = Driver(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=email,
                address = fake.address(),
                carrier_id=choice(carriers).carrier_id,
                emergency_contact = f"+2547{randint(00_000_000, 99_999_999):08d}",
                license_number=f"ABC{randint(1000,9999)}",
                license_expiry=datetime.utcnow() + timedelta(days=365),
                license_type=f"Class {choice(['A', 'B', 'C'])}",
                contact_phone=f"+2547{randint(00_000_000, 99_999_999):08d}",
                medical_certificate_expiry=datetime.utcnow() + timedelta(days=randint(10,360)),
                status=f"{choice(['active', 'inactive'])}",
                training_certifications= choice( [
                                        "First Aid Training",
                                        "Defensive Driving",
                                        "Hazardous Materials Handling",
                                        "Customer Service Excellence",
                                        "Vehicle Maintenance Basics",
                                        "Logistics & Supply Chain Essentials",
                                        "Road Safety Awareness",
                                        "Fleet Management Certificate"
                                    ]),
                created_at=datetime.now(timezone.utc) + timedelta(days=choice([0,30,60,90])),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(driver)
            logger.info(f"Driver {email} seeded successfully.")
        else:
            logger.info(f"Driver {email} already exists.")
    db.session.commit()  
    seed_driver_schedule()  

def seed_clients():
    # try:
    #     # client = Client.query.filter_by(email="client1@example.com").first()
    #     if not client:
    #         client = Client(
    #             company_name=fake.company(),
    #             contact_person=fake.name(),
    #             email=fake.email(),
    #             phone=f"+2547{randint(00_000_000, 99_999_999):08d}",
    #             address=fake.address(),
    #             tax_id=randint(100000000, 999999999),
    #             registration_number=f"REG{randint(10000,99999)}",
    #             account_status=choice(["active", "inactive"]),
    #             credit_limit=fake.pyfloat(left_digits=5, right_digits=2, positive=True),
    #             payment_terms=choice(["Net 15", "Net 30", "Net 45"]),
    #         )
    #         db.session.add(client)
    #         logger.info("Client seeded successfully.")
    #     else:
    #         logger.info("Client already exists.")
    # except Exception as e:
    #     logger.error(f"Error seeding client: {e}")
    
    for i in range(1, 21): 
        try:
            client = Client(
                company_name=fake.company(),
                contact_person=fake.name(),
                email=fake.email(),
                phone=f"+2547{randint(00_000_000, 99_999_999):08d}",
                address=fake.address(),
                tax_id=randint(100000000, 999999999),
                registration_number=f"REG{randint(10000,99999)}",
                account_status=choice(["active", "inactive"]),
                credit_limit=fake.pyfloat(left_digits=5, right_digits=2, positive=True),
                payment_terms=choice(["Net 15", "Net 30", "Net 45"]),
            )
            db.session.add(client)
        except Exception as e:
            logger.error(f"Error seeding client: {e}")

    logger.info("Client seeded successfully.")


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
            order_date=datetime.now(timezone.utc),
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


def seed_vehicles():
    vehicle = Vehicle.query.filter_by(registration_number="KAA123A").first()
    if not vehicle:
        carrier = Carrier.query.first()
        location = Location.query.first()

        if not carrier:
            logger.warning("No carrier found to associate with vehicle.")
            return
        if not location:
            logger.warning("No location found to associate with vehicle.")
            return

        vehicle = Vehicle(
            registration_number="KAA123A",
            vehicle_type="Truck",
            make="Toyota",
            model="Hilux",
            year=2020,
            max_weight_capacity=1500.0,
            max_volume_capacity=12.5,
            carrier_id=carrier.carrier_id,
            current_location_id=location.location_id,
            status="active",
            insurance_expiry=datetime.utcnow() + timedelta(days=365),
            last_maintenance_date=datetime.utcnow() - timedelta(days=30),
            next_maintenance_date=datetime.utcnow() + timedelta(days=60)
        )
        vehicle.validate_vehicle()  
        db.session.add(vehicle)
        logger.info("Vehicle seeded successfully.")
    else:
        logger.info("Vehicle already exists.")


# def seed_carriers():
#     carrier = Carrier.query.filter_by(carrier_name="Example Carrier").first()
#     if not carrier:
#         carrier = Carrier(
#             carrier_name="Example Carrier",
#             carrier_type="Freight",
#             contact_person="John Smith",
#             phone="+254700123456",
#             email="carrier@example.com",
#         )
#         db.session.add(carrier)
#         logger.info("Carrier seeded successfully.")
#     else:
#         logger.info("Carrier already exists.")


def seed_shipments():
    shipment = Shipment.query.filter_by(shipment_reference="SHIP001").first()
    if not shipment:
        carrier = Carrier.query.first()
        location = Location.query.first()
        if not carrier or not location:
            logger.warning("Cannot seed Shipment - missing carrier or location.")
            return
        shipment = Shipment(
            shipment_reference="SHIP001",
            carrier_id=carrier.carrier_id,
            origin_location_id=location.location_id,
            destination_location_id=location.location_id,
            status=ShipmentStatusEnum.IN_TRANSIT,
            shipping_method=ShippingMethodEnum.AIR,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(shipment)
        logger.info("Shipment seeded successfully.")
    else:
        logger.info("Shipment already exists.")


def seed_tracking_events():
    tracking_event = TrackingEvent.query.first()
    if not tracking_event:
        shipment = Shipment.query.first()
        location = Location.query.first()

        if not shipment or not location:
            logger.warning("Cannot seed TrackingEvent - missing shipment or location.")
            return

        with db.session.no_autoflush:
            tracking_event = TrackingEvent(
                shipment_id=UUID(str(shipment.shipment_id)) if not isinstance(shipment.shipment_id, UUID) else shipment.shipment_id,
                event_type="DELIVERED",
                event_time=datetime.now(timezone.utc),  
                location_id=UUID(str(location.location_id)) if not isinstance(location.location_id, UUID) else location.location_id,
                gps_coordinates="1.2921,36.8219",  
                event_description="Package delivered at final destination.",
                recorded_by="admin@example.com"
            )
            db.session.add(tracking_event)
            db.session.commit()
            logger.info("TrackingEvent seeded successfully.")
    else:
        logger.info("TrackingEvent already exists.")


def seed_warehouse_operations():
    from uuid import uuid4
    operation = WarehouseOperation.query().filter_by(reference_id=uuid4()).first()  
    reference_id_to_seed = uuid4()
    operation = WarehouseOperation.query().filter_by(reference_id=reference_id_to_seed).first()
    if not operation:
        location = Location.query.first()
        operator = Employee.query.first()  
        if not location or not operator:
            logger.warning("Cannot seed WarehouseOperation - missing location or operator.")
            return
        operation = WarehouseOperation(
            reference_id=reference_id_to_seed,
            operation_type="LOADING",
            status=OperationStatus.COMPLETED,
            location_id=location.location_id,
            operator_id=operator.employee_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(operation)
        logger.info("WarehouseOperation seeded successfully.")
    else:
        logger.info("WarehouseOperation already exists.")


def main():
    logger.info("Starting database seeding...")
    models = [System_Users, Driver, Client, Location, Order, Product, Vehicle, Carrier, Shipment, DriverSchedule, WarehouseOperation, TrackingEvent]

    for model in models:
        db.session.query(model).delete()

    db.session.commit()
    seed_admin_user()
    seed_carriers()
    seed_drivers()
    seed_driver_schedule()
    seed_clients()
    seed_locations()
    seed_orders()
    seed_products()
    seed_vehicles()
    seed_carriers()
    seed_shipments()
    seed_tracking_events()
    seed_warehouse_operations()
    db.session.commit()
    logger.info("Database seeding completed successfully.")


if __name__ == "__main__":
    from app import app
    with app.app_context():
        main()
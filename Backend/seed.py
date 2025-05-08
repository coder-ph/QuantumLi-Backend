import os
from datetime import datetime, timedelta, timezone
from uuid import UUID
from dotenv import load_dotenv
import os
from sqlalchemy.sql import func
from src.startup.database import db
from src.Models.systemusers import System_Users
from src.Models.drivers import Driver
from src.Models.orders import Order, OrderStatus, BillingType, PaymentStatus
from src.Models.locations import Location
from src.Models.driverSchedule import DriverSchedule
from src.Models.billing import Billing
from src.Models.product import Product
from src.Models.documents import Document
from src.Models.audit_logs import Audit_Logs
from src.Models.customerfeedback import Customer_Feedback
from src.Models.inventory import Inventory
from src.Models.shipment import Shipment, ShipmentStatusEnum, ShippingMethodEnum
from src.Models.carriers import Carrier
from src.Models.notification import Notifications
from src.Models.orderItem import OrderItem
from src.Models.invoiceitems import InvoiceItems
from src.Models.shipmentOrder import ShipmentOrder
from src.Models.trackevents import TrackingEvent
from src.Models.driverRating import Driver_Ratings
from src.Models.warehouseOperations import WarehouseOperation, OperationStatus
from src.Models.client import Client
from src.Models.rates import Rates
from src.Models.thirdparty import ThirdPartyService
from src.Models.incidents import Incidents
from src.Models.inventoryMovement import InventoryMovement, MovementType
from src.Models.vehicles import Vehicle
from src.Models.orders import Order
from src.Models.orderResponse import OrderResponse,ResponseStatus
from src.Models.employee import Employee
from src.utils.logger import logger
from werkzeug.security import generate_password_hash

from faker import Faker #type: ignore
from random import randint, choice, uniform, sample
import json
import uuid
from uuid import uuid4


fake = Faker()

def seed_order_responses():

    orders = Order.query.all()
    drivers = Driver.query.all()

    if not orders or not drivers:
        logger.warning("Cannot seed OrderResponse: No orders or drivers available.")
        return

    for i in range(1, 31): 
        order = choice(orders)
        driver = choice(drivers)
        status = choice([ResponseStatus.ACCEPTED, ResponseStatus.REJECTED])
        reason = None if status == ResponseStatus.ACCEPTED else fake.sentence(nb_words=6)

        response = OrderResponse(
            order_id=order.order_id,
            driver_id=driver.driver_id,
            status=status,
            reason=reason,
            responded_at=fake.date_time_between(start_date='-30d', end_date='now')
        )

        try:
            db.session.add(response)
            db.session.commit()
            logger.info(f"OrderResponse for order {order.order_id} and driver {driver.driver_id} created.")
        except Exception as e:
            logger.error(f"Failed to create OrderResponse: {e}")
            db.session.rollback()


def seed_orders():
    clients = Client.query.all()
    logger.info(f"{len(clients)} clients found for orders.")
    if not clients:
        logger.warning("Cannot seed orders: No clients found.")
        return

    for _ in range(20):  
        client = choice(clients)
        order_date = fake.date_between(start_date='-60d', end_date='today')
        pickup_date = order_date + timedelta(days=1)
        delivery_date = pickup_date + timedelta(days=choice([1, 2, 3, 5]))

        order = Order(
            order_id=uuid.uuid4(),
            client_id=client.client_id,
            order_reference=fake.unique.bothify(text="ORD-####-??"),
            order_date=order_date,
            requested_pickup_date=pickup_date,
            requested_delivery_date=delivery_date,
            priority=choice(['Low', 'Medium', 'High', 'Critical']),
            special_instructions=fake.sentence(nb_words=8),
            status=choice(list(OrderStatus)),
            billing_type=choice(list(BillingType)),
            payment_status=choice(list(PaymentStatus)),
            total_weight=round(uniform(100.0, 1000.0), 2),  
            total_volume=round(uniform(1.0, 20.0), 2),     
            declared_value=round(uniform(1000.0, 10000.0), 2),
            required_documents=fake.sentence(nb_words=6)
        )

        try:
            db.session.add(order)
            db.session.commit()
            logger.info(f"Order {order.order_reference} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed order: {e}")


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
                "monday": {"work": choice([True,False]), "start": f"{random_time_between('06:00', '10:00')}", "end": f"{random_time_between('15:00', '20:00')}"},
                "tuesday": {"work": choice([True,False]), "start": f"{random_time_between('06:00', '10:00')}", "end": f"{random_time_between('15:00', '20:00')}"},
                "wednesday": {"work": choice([True,False]), "start":f"{random_time_between('06:00', '10:00')}", "end": f"{random_time_between('15:00', '20:00')}"},
                "thursday": {"work": choice([True,False]), "start": f"{random_time_between('06:00', '10:00')}", "end": f"{random_time_between('15:00', '20:00')}"},
                "friday": {"work": choice([True,False]), "start": f"{random_time_between('06:00', '10:00')}", "end": f"{random_time_between('15:00', '20:00')}"},
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

    db.session.commit()
    logger.info("Client seeded successfully.")

def seed_products():
    clients = Client.query.all()

    if not clients:
        logger.warning("Cannot seed products: No clients found.")
        return

    for _ in range(50):  
        client = choice(clients)

        product = Product(
            client_id=client.client_id,
            sku=fake.unique.bothify(text="SKU-?????-???"),
            name=fake.word().capitalize() + " " + fake.word().capitalize(),
            description=fake.sentence(nb_words=10),
            category=choice(['Electronics', 'Clothing', 'Furniture', 'Food', 'Toys']),
            weight=round(uniform(0.5, 100.0), 2),
            dimensions=f"{randint(10, 100)}x{randint(10, 100)}x{randint(10, 100)}", 
            unit_volume=round(uniform(0.01, 10.0), 2),
            hazardous=choice([True, False]),
            perishable=choice([True, False]),
            temperature_requirements=choice(['Cold', 'Room Temp', 'Frozen', None]),
            handling_requirements=fake.sentence(nb_words=6),
            customs_tariff_code=fake.word().upper(),
            value=round(uniform(5.0, 500.0), 2)
        )

        try:
            db.session.add(product)
            db.session.commit()
            logger.info(f"Product {product.sku} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed product: {e}")

def seed_billing():
    clients = Client.query.all()
    if not clients:
        logger.warning("Cannot seed billing: No clients found.")
        return

    for _ in range(20):
        client = choice(clients)

        invoice_date = fake.date_between(start_date='-60d', end_date='today')
        due_date = invoice_date + timedelta(days=choice([15, 30, 45]))
        total_amount = round(uniform(1000.0, 10000.0), 2)
        tax_amount = round(total_amount * 0.16, 2) 

        billing = Billing(
            client_id=client.client_id,
            invoice_date=invoice_date,
            due_date=due_date,
            total_amount=total_amount,
            tax_amount=tax_amount,
            status=choice(['draft', 'paid', 'overdue']),
            payment_date=invoice_date + timedelta(days=choice([15, 30])) if choice([True, False]) else None,
            payment_method=choice(['MPESA', 'Bank Transfer', 'Credit Card', None]),
            reference_numbers=fake.bothify(text='INV-####-??'),
            notes=fake.sentence(nb_words=6),
        )

        try:
            db.session.add(billing)
            db.session.commit()
            logger.info(f"Billing invoice for client {client.company_name} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed billing invoice: {e}")

def seed_audit_logs():
    users = System_Users.query.all()
    if not users:
        logger.warning("Cannot seed audit logs: No system users found.")
        return

    action_types = ["CREATE", "UPDATE", "DELETE", "LOGIN", "LOGOUT"]
    tables = ["clients", "orders", "billing", "products", "shipments"]

    for _ in range(30):
        user = choice(users)
        action_type = choice(action_types)
        affected_table = choice(tables)

        log = Audit_Logs(
            user_id=user.user_id,
            action_type=action_type,
            affected_table=affected_table,
            record_id=uuid.uuid4(),
            action=f"{action_type} operation on {affected_table}",
            timestamp=fake.date_time_between(start_date='-30d', end_date='now'),
            ip_address=fake.ipv4_public(),
            user_agent=fake.user_agent(),
            description=fake.sentence(nb_words=8)
        )

        try:
            db.session.add(log)
            db.session.commit()
            logger.info(f"Audit log for user {user.username} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed audit log: {e}")

def seed_customer_feedback():
    clients = Client.query.all()
    order_items = OrderItem.query.all()

    if not clients or not order_items:
        logger.warning("Cannot seed feedback: Clients or Order Items not found.")
        return

    for _ in range(30):
        client = choice(clients)
        order_item = choice(order_items)

        feedback = Customer_Feedback(
            client_id=client.client_id,
            order_item_id=order_item.order_item_id,
            rating=randint(1, 5),
            comments=fake.sentence(nb_words=10),
            feedback_date=fake.date_between(start_date='-30d', end_date='today'),
            follow_up_required=choice([True, False]),
            follow_up_status=choice(["Pending", "In Progress", "Resolved", None]),
            is_deleted=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        try:
            db.session.add(feedback)
            db.session.commit()
            logger.info(f"Feedback from client {client.company_name} added.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed customer feedback: {e}")

def seed_order_items():
    orders = Order.query.all()
    products = Product.query.all()
    inventories = Inventory.query.all()

    if not orders or not products:
        logger.warning("Cannot seed order items: Orders or Products not found.")
        return

    for _ in range(50):  # You can adjust the number to seed more/less items
        order = choice(orders)
        product = choice(products)
        inventory_source = choice(inventories) if inventories else None

        order_item = OrderItem(
            order_id=order.order_id,
            product_id=product.product_id,
            quantity=randint(1, 10),
            unit_weight=round(uniform(1.0, 50.0), 2),  # Adjust the range based on your needs
            unit_volume=round(uniform(0.1, 20.0), 2),  # Adjust the range based on your needs
            handling_instructions=fake.sentence(nb_words=6),
            inventory_source_id=inventory_source.inventory_id if inventory_source else None
        )

        try:
            db.session.add(order_item)
            db.session.commit()
            logger.info(f"Order Item {order_item.order_item_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed order item: {e}")

def seed_inventory():
    products = Product.query.all()
    locations = Location.query.all()

    if not products or not locations:
        logger.warning("Cannot seed inventory: No products or locations found.")
        return

    for _ in range(50):  
        product = choice(products)
        location = choice(locations)

        inventory_item = Inventory(
            product_id=product.product_id,
            location_id=location.location_id,
            quantity_on_hand=randint(1, 100), 
            quantity_allocated=randint(0, 50), 
            quantity_on_order=randint(0, 20),  
            last_stock_take_date=fake.date_this_year(),  
            bin_location=fake.word().upper() + str(randint(1, 100)),
            batch_number=fake.bothify(text="BATCH-???-####"), 
            expiry_date=fake.date_between(start_date='today', end_date='+2y') 
        )

        try:
            db.session.add(inventory_item)
            db.session.commit()
            logger.info(f"Inventory for product {product.sku} at location {location.location_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed inventory: {e}")

def seed_driver_ratings():
    drivers = Driver.query.all()  
    order_items = OrderItem.query.all()  
    clients = Client.query.all()  

    if not drivers or not order_items or not clients:
        logger.warning("Cannot seed driver ratings: Missing data (drivers, order items, or clients).")
        return

    for _ in range(50):  
        driver = choice(drivers)
        order_item = choice(order_items)
        client = choice(clients)

        rating = randint(1, 5)  

        driver_rating = Driver_Ratings(
            driver_id=driver.driver_id,
            order_item_id=order_item.order_item_id,
            rating=rating,
            comments=fake.sentence(nb_words=10),  
            rating_date=fake.date_this_year(),  
            follow_up_required=choice([True, False]),
            follow_up_status=choice(['open', 'resolved', 'pending']),
            client_id=client.client_id,
            is_deleted=False
        )

        try:
            db.session.add(driver_rating)
            db.session.commit()
            logger.info(f"Driver rating for driver {driver.driver_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed driver rating: {e}")

def seed_documents():
    drivers = Driver.query.all()  

    if not drivers:
        logger.warning("Cannot seed documents: No drivers found.")
        return

    document_types = ['License', 'Insurance', 'Permit', 'ID Card']  

    for _ in range(30):  
        driver = choice(drivers)

        document = Document(
            document_name=fake.word().capitalize() + " " + choice(document_types), 
            driver_id=driver.driver_id,
            type=choice(document_types),  
            file_url=fake.url(),  
            status=choice(['pending', 'approved', 'rejected']),  
            uploaded_at=fake.date_this_year(),  
            expiry_date=fake.date_between(start_date='today', end_date='+2y')  
        )

        try:
            db.session.add(document)
            db.session.commit()
            logger.info(f"Document {document.document_name} for driver {driver.driver_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed document: {e}")

def seed_employees():
    positions = ['Manager', 'Developer', 'Driver', 'Sales', 'HR', 'Finance', 'Admin']
    departments = ['IT', 'Sales', 'HR', 'Finance', 'Operations']
    access_levels = ['Admin', 'User', 'Manager']
    
    for _ in range(20):  
        supervisor = None
        
        if _ > 0:  
            supervisor = Employee.query.order_by(func.random()).first()

        employee = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            position=choice(positions),
            department=choice(departments),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            hire_date=fake.date_this_decade(),
            termination_date=None if choice([True, False]) else fake.date_this_year(),  
            supervisor_id=supervisor.employee_id if supervisor else None,
            access_level=choice(access_levels),
            login_credentials=fake.password(),
            is_deleted=False
        )

        try:
            db.session.add(employee)
            db.session.commit()
            logger.info(f"Employee {employee.first_name} {employee.last_name} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed employee: {e}")

def seed_incidents():
    for _ in range(20):  
        try:
            incident = Incidents(
                incident_id=uuid4(),
                related_to=choice(['shipment', 'order']),
                related_id=uuid4(),  
                incident_type=choice(['damage', 'delay', 'loss', 'theft']),
                severity=choice(['high', 'medium', 'low']),
                description=fake.text(),  
                reported_by=fake.name(),  
                report_date=fake.date_this_year(),  
                resolution_status=choice(['open', 'resolved', 'pending']),
                resolution_details=fake.text() if choice([True, False]) else None,  
                compensation_amount=uniform(100, 1000) if choice([True, False]) else None,  
            )
            db.session.add(incident)
            db.session.commit()
            logger.info(f"Incident {incident.incident_id} seeded successfully.")
        
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed incident: {e}")

    logger.info("Incidents seeded successfully.")

def seed_inventory_movements():
    locations = Location.query.all()
    for _ in range(20):  
        try:
            location1 = choice(locations)
            location2 = choice(locations)

            movement = InventoryMovement(
                movement_id=uuid4(),
                product_id=uuid4(),  
                from_location_id=location1.location_id,
                to_location_id=location2.location_id,  
                quantity=randint(1, 100),
                movement_type=choice([MovementType.RECEIPT, MovementType.SHIPMENT, MovementType.TRANSFER]),
                reference_id=uuid4() if choice([True, False]) else None, 
                reference_type=fake.word() if choice([True, False]) else None,  
                movement_date=fake.date_this_year(),  
                recorded_by=fake.name(),  
                batch_number=fake.word() if choice([True, False]) else None, 
                expiry_date=fake.date_this_year() if choice([True, False]) else None, 
            )
            db.session.add(movement)
            db.session.commit()
            logger.info(f"Movement {movement.movement_id} seeded successfully.")
        
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed movement: {e}")

    logger.info("Inventory movements seeded successfully.")

def seed_invoice_items():
    for _ in range(20):  
        try:
            quantity = round(uniform(1, 10), 2)
            unit_price = round(uniform(100, 1000), 2)
            tax_rate = round(uniform(0.05, 0.20), 2)
            total_price = round(quantity * unit_price * (1 + tax_rate), 2)

            item = InvoiceItems(
                invoice_item_id=uuid4(),
                invoice_id=uuid4(),  
                item_description=fake.sentence(nb_words=4),
                related_to=choice(['shipment', 'storage', 'handling', 'other']),
                related_id=uuid4(), 
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                tax_rate=tax_rate,
            )
            db.session.add(item)
            db.session.commit()
            logger.info(f"Invoice item {item.invoice_item_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Seeding failed: {e}")

    logger.info("Invoice items seeded successfully.")


def seed_locations():
    location_types = ['warehouse', 'hub', 'customer', 'other']

    for _ in range(20):  
        try:
            location = Location(
                location_id=uuid4(),
                location_name=fake.company(),
                location_type=choice(location_types),
                address=fake.street_address(),
                city=fake.city(),
                state_province=fake.state(),
                postal_code=fake.postcode(),
                country=fake.country(),
                contact_person=fake.name(),
                contact_phone=f"+2547{randint(00_000_000, 99_999_999):08d}",
                operating_hours="08:00 - 18:00",
                latitude=round(uniform(-90.0, 90.0), 6),
                longitude=round(uniform(-180.0, 180.0), 6),
                is_active=True
            )
            db.session.add(location)
            db.session.commit()
            logger.info(f"Location {location.location_name} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Seeding failed: {e}")

    logger.info("Locations seeded successfully.")

def seed_notifications():
    statuses = ['sent', 'read', 'unread', 'failed']
    types = ['shipment_update', 'invoice_alert', 'system_notice', 'reminder']

    for _ in range(30):
        try:
            notification = Notifications(
                notification_id=uuid4(),
                recipient_id=uuid4(),  
                message=fake.sentence(nb_words=10),
                type=choice(types),
                status=choice(statuses),
                created_at=fake.date_time_this_year(),
                read_at=fake.date_time_this_year() if choice([True, False]) else None,
                related_entity=choice(['shipment', 'invoice', 'user']) if choice([True, False]) else None,
                related_id=uuid4() if choice([True, False]) else None
            )
            db.session.add(notification)
            db.session.commit()
            logger.info(f"Notification {notification.notification_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Seeding notification failed: {e}")

    logger.info("Notifications seeded successfully.")

def seed_rates():
    service_types = ['air', 'road', 'sea', 'rail']
    zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D']
    weight_breaks = ['0-5kg', '5-10kg', '10-20kg']
    volume_breaks = ['0-0.5cbm', '0.5-1cbm', '1-2cbm']

    clients = Client.query.all()

    for _ in range(20):
        try:
            client = choice(clients)
            rate = Rates(
                rate_id=uuid4(),
                client_id=client.client_id,
                rate_name=fake.word().capitalize() + " Rate",
                effective_date=fake.date_this_decade(),
                expiry_date=fake.date_between(start_date='today', end_date='+1y') if choice([True, False]) else None,
                service_type=choice(service_types),
                origin_zone=choice(zones),
                destination_zone=choice(zones),
                weight_break=choice(weight_breaks),
                volume_break=choice(volume_breaks),
                rate_per_unit=round(uniform(10, 500), 2),
                minimum_charge=round(uniform(5, 50), 2),
                accessorial_charges=round(uniform(1, 20), 2) if choice([True, False]) else None
            )
            db.session.add(rate)
            db.session.commit()
            logger.info(f"Rate {rate.rate_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Seeding rate failed: {e}")

    logger.info("Rates seeded successfully.")

def seed_shipment_orders():
    shipments = Shipment.query.all()
    orders = Order.query.all()

    if not shipments or not orders:
        logger.warning("No shipments or orders found to associate with shipment orders.")
        return

    for _ in range(20):
        try:
            shipment = choice(shipments)
            order = choice(orders)
            loading_seq = randint(1, 5)
            unloading_seq = loading_seq + randint(1, 5)

            shipment_order = ShipmentOrder(
                shipment_order_id=uuid4(),
                shipment_id=shipment.shipment_id,
                order_id=order.order_id,
                loading_sequence=loading_seq,
                unloading_sequence=unloading_seq,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.session.add(shipment_order)
            db.session.commit()
            logger.info(f"ShipmentOrder {shipment_order.shipment_order_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Seeding ShipmentOrder failed: {e}")

    logger.info("Shipment orders seeded successfully.")

def seed_shipments():
    orders = Order.query.all()
    carriers = Carrier.query.all()
    vehicles = Vehicle.query.all()
    drivers = Driver.query.all()
    locations = Location.query.all()

    if len(locations) < 2:
        logger.warning("Not enough locations to create shipments.")
        return

    for _ in range(20):
        try:
            origin, destination = sample(locations, 2)

            shipment = Shipment(
                shipment_id=uuid4(),
                shipment_reference=f"SHIP-{uuid4().hex[:8].upper()}",
                order_id=choice(orders).order_id if orders else None,
                carrier_id=choice(carriers).carrier_id if carriers else None,
                vehicle_id=choice(vehicles).vehicle_id if vehicles else None,
                driver_id=choice(drivers).driver_id if drivers else None,
                origin_location_id=origin.location_id,
                destination_location_id=destination.location_id,
                planned_departure=datetime.utcnow() + timedelta(days=1),
                planned_arrival=datetime.utcnow() + timedelta(days=5),
                actual_departure=None,
                actual_arrival=None,
                status=ShipmentStatusEnum.PLANNED,
                shipping_method=choice(list(ShippingMethodEnum)),
                tracking_number=f"TRK-{uuid4().hex[:10].upper()}",
                total_weight=round(uniform(100.0, 5000.0), 2),
                total_volume=round(uniform(1.0, 50.0), 2),
                bill_of_lading_number=f"BOL-{uuid4().hex[:6].upper()}",
                shipping_cost=round(uniform(100.0, 10000.0), 2),
                fuel_surcharge=round(uniform(10.0, 500.0), 2),
                accessorial_charges=round(uniform(0.0, 200.0), 2),
                temperature_monitoring=choice([True, False]),
                seal_number=f"SEAL-{uuid4().hex[:5].upper()}"
            )

            db.session.add(shipment)
            db.session.commit()
            logger.info(f"Shipment {shipment.shipment_reference} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Seeding shipment failed: {e}")

    logger.info("Shipments seeded successfully.")

def seed_system_users():
    roles = ['admin', 'employee', 'driver', 'user', 'manager']
    for _ in range(10):
        try:
            password = os.getenv("SEED_PASSWORD")
            user = System_Users(
                user_id=uuid4(),
                username=fake.user_name(),
                password_hash=generate_password_hash(password),
                email=fake.unique.email(),
                phone=int(fake.msisdn()[:10]),
                role=choice(roles),
                last_login=fake.date_time_between(start_date='-30d', end_date='now'),
                is_active=True,
                status=choice(['active', 'pending', 'suspended']),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Seeded user: {user.username}")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed user: {e}")

def seed_third_party_services():
    authentication_methods = ['api_key', 'oauth2', 'basic_auth', 'jwt']
    for _ in range(10):  
        try:
            service = ThirdPartyService(
                service_id=uuid4(),
                service_name=fake.company(),
                type=choice(['Payment Gateway', 'Shipping Service', 'CRM', 'Analytics', 'Cloud Storage']),
                contact_info=fake.email(),
                authentication_method=choice(authentication_methods),
                config_details=json.dumps({
                    'api_endpoint': fake.url(),
                    'api_key': fake.uuid4(),
                    'timeout': choice([30, 60, 120]),
                    'retry_limit': choice([3, 5, 10])
                }),
                active_status=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(service)
            db.session.commit()
            logger.info(f"Seeded third-party service: {service.service_name}")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed third-party service: {e}")


def seed_tracking_events():
    shipments = Shipment.query.all()  
    locations = Location.query.all()  

    event_types = ['pickup', 'in_transit', 'delivery', 'delayed', 'customs_clearance']
    
    for _ in range(20):  
        try:
            shipment = choice(shipments)  
            location = choice(locations)  

            event_time = fake.date_this_year() + timedelta(hours=fake.random_int(min=0, max=24))  
            gps_coordinates = f"{fake.latitude()}, {fake.longitude()}"  

            tracking_event = TrackingEvent(
                tracking_event_id=uuid4(),
                shipment_id=shipment.shipment_id,
                event_type=choice(event_types),
                event_time=event_time,
                location_id=location.location_id,
                gps_coordinates=gps_coordinates,
                event_description=fake.sentence(),
                recorded_by=fake.name(),
                signature=fake.word() if choice([True, False]) else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.session.add(tracking_event)
            db.session.commit()
            logger.info(f"Tracking event {tracking_event.tracking_event_id} seeded for shipment {shipment.shipment_reference}.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed tracking event: {e}")

    logger.info("Tracking events seeded successfully.")


def seed_vehicles():
    carriers = Carrier.query.all()  
    locations = Location.query.all()  

    vehicle_types = ['truck', 'van', 'bus', 'sedan', 'motorcycle']
    vehicle_status = ['active', 'inactive', 'maintenance', 'retired']
    
    for _ in range(20):  
        try:
            carrier = choice(carriers) if carriers else None
            location = choice(locations) if locations else None  

            last_maintenance_date = fake.date_this_decade()
            next_maintenance_date = fake.date_this_decade()
            insurance_expiry = fake.date_this_year()

            vehicle = Vehicle(
                vehicle_id=uuid4(),
                carrier_id=carrier.carrier_id if carrier else None,
                registration_number=fake.license_plate(),
                vehicle_type=choice(vehicle_types),
                make=fake.company(),
                model=fake.word(),
                year=fake.year(),
                max_weight_capacity=fake.random_int(min=500, max=5000),
                max_volume_capacity=fake.random_int(min=10, max=100),  
                current_location_id=location.location_id if location else None,
                status=choice(vehicle_status),
                last_maintenance_date=last_maintenance_date,
                next_maintenance_date=next_maintenance_date,
                insurance_expiry=insurance_expiry,
            )
            db.session.add(vehicle)
            db.session.commit()
            logger.info(f"Vehicle {vehicle.registration_number} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed vehicle: {e}")

    logger.info("Vehicles seeded successfully.")


def seed_warehouse_operations():
    locations = Location.query.all()  
    employees = Employee.query.all()  

    operation_types = ['receiving', 'picking', 'packing', 'shipping', 'inventory']
    equipment_types = ['forklift', 'pallet jack', 'hand truck', 'conveyor belt', 'robot arm']
    
    for _ in range(20):
        try:
            location = choice(locations)  
            operator = choice(employees)  

            start_time = fake.date_this_year()
            end_time = fake.date_this_year() if choice([True, False]) else None

            warehouse_operation = WarehouseOperation(
                operation_id=uuid4(),
                location_id=location.location_id,
                operation_type=choice(operation_types),
                    reference_id=uuid4(),  
                start_time=start_time,
                end_time=end_time,
                operator_id=operator.employee_id,
                status=choice([status for status in OperationStatus]),
                equipment_used=choice(equipment_types) ,
                notes=fake.text() ,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.session.add(warehouse_operation)
            db.session.commit()
            logger.info(f"Warehouse operation {warehouse_operation.operation_id} seeded.")
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Failed to seed warehouse operation: {e}")

    logger.info("Warehouse operations seeded successfully.")

def main():
    logger.info("Starting database seeding...")
    models = [System_Users, Customer_Feedback, ShipmentOrder, WarehouseOperation, System_Users, Vehicle, ThirdPartyService ,TrackingEvent, Shipment, Notifications, Rates, Location, InvoiceItems, InventoryMovement, Document, Incidents, Driver_Ratings, OrderItem, Driver, Billing, Inventory, Client, Audit_Logs, Location, Order, Product, Vehicle, Carrier, Shipment, DriverSchedule, WarehouseOperation, OrderResponse,TrackingEvent]

    for model in models:
        db.session.query(model).delete()

    db.session.commit()
    seed_vehicles()
    seed_admin_user()
    seed_carriers()
    seed_drivers()
    seed_driver_schedule()
    seed_clients()
    seed_locations()
    seed_orders()
    seed_products()
    seed_carriers()
    seed_order_responses()
    seed_billing()
    seed_audit_logs()
    seed_inventory()
    seed_order_items()
    seed_customer_feedback()
    seed_driver_ratings()
    seed_documents()
    seed_employees()
    seed_incidents()
    seed_locations()
    seed_inventory_movements()
    seed_notifications()
    seed_rates()
    seed_shipment_orders()
    seed_shipments()
    seed_system_users()
    seed_third_party_services()
    seed_tracking_events()
    seed_warehouse_operations()
    db.session.commit()
    logger.info("Database seeding completed successfully.")


if __name__ == "__main__":
    from app import app
    with app.app_context():
        main()
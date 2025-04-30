from flask_migrate import Migrate
from src.utils.logger import logger
from src.config.redis_config import init_redis, init_pubsub

class Models:
    def __init__(self, db):
        self.db = db
       
        self.audit_logs = None
        self.base_model = None
        self.billing = None
        self.client = None
        self.carrier = None
        self.customer_feedback = None
        self.driver_ratings = None
        # self.driver_location = None
        self.driver = None
        self.driver_schedule = None
        self.system_users = None
        self.employee = None
        self.incidents = None
        self.inventory = None
        self.inventory_movement = None
        self.invoice_items = None
        self.location = None
        self.notifications = None
        self.order_item = None
        self.order = None
        self.product = None
        self.rates = None
        self.shipment = None
        self.shipment_order = None
        self.third_party = None
        self.tracking_event = None
        self.vehicle = None
        self.warehouse_operation = None

    def init_app(self, app):
        
    
        with app.app_context():
           
            from src.Models.audit_logs import Audit_Logs
            from src.Models.base_model import BaseModel
            from src.Models.carriers import Carrier
            from src.Models.billing import Billing
            from src.Models.client import Client
            from src.Models.customerfeedback import Customer_Feedback
            from src.Models.driverRating import Driver_Ratings
            # from src.Models.driverLocation import DriverLocation
            from src.Models.drivers import Driver
            from src.Models.driverSchedule import DriverSchedule
            from src.Models.systemusers import System_Users
            from src.Models.employee import Employee
            self.employee = Employee
            from src.Models.incidents import Incidents
            from src.Models.inventory import Inventory
            from src.Models.inventoryMovement import InventoryMovement
            from src.Models.invoiceitems import InvoiceItems
            from src.Models.locations import Location
            from src.Models.notification import Notifications
            from src.Models.orderItem import OrderItem
            from src.Models.orders import Order
            from src.Models.product import Product
            from src.Models.rates import Rates
            from src.Models.shipment import Shipment
            from src.Models.shipmentOrder import ShipmentOrder
            from src.Models.thirdparty import ThirdPartyService
            from src.Models.trackevents import TrackingEvent
            from src.Models.vehicles import Vehicle
            from src.Models.warehouseOperations import WarehouseOperation
            

            self.audit_logs = Audit_Logs
            self.base_model = BaseModel
            self.billing = Billing
            self.client = Client
            self.carrier = Carrier
            self.customer_feedback = Customer_Feedback
            self.driver_ratings = Driver_Ratings
            # self.driver_location = DriverLocation
            self.driver = Driver
            self.driver_schedule = DriverSchedule
            self.system_users = System_Users
            self.incidents = Incidents
            self.inventory = Inventory
            self.inventory_movement = InventoryMovement
            self.invoice_items = InvoiceItems
            self.location = Location
            self.notifications = Notifications
            self.order_item = OrderItem
            self.order = Order
            self.product = Product
            self.rates = Rates
            self.shipment = Shipment
            self.shipment_order = ShipmentOrder
            self.third_party = ThirdPartyService
            self.tracking_event = TrackingEvent
            self.vehicle = Vehicle
            self.warehouse_operation = WarehouseOperation

            redis_client = init_redis()
            pubsub = init_pubsub()
            migrate = Migrate(app, self.db)

            logger.info("Models initialized successfully.")
            logger.info("App initialized with Models, Redis, and Migrate.")

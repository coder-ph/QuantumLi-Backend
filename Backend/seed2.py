import logging
from datetime import datetime
from random import choice, randint
from faker import Faker
from src.startup.database import db
from src.Models.orderResponse import OrderResponse, ResponseStatus
from src.Models.orders import Order
from src.Models.drivers import Driver
from app import app

fake = Faker()
logger = logging.getLogger(__name__)

def seed_order_responses(num_entries=50):
    with app.app_context():
        orders = [o for (o,) in db.session.query(Order).all()]
        drivers = [d for (d,) in db.session.query(Driver).all()]

        if not orders:
            logger.warning("No orders found to link order responses.")
            return
        if not drivers:
            logger.warning("No drivers found to link order responses.")
            return

        for _ in range(num_entries):
            order = choice(orders)
            driver = choice(drivers)
            status = choice([ResponseStatus.ACCEPTED, ResponseStatus.REJECTED])
            reason = None
            if status == ResponseStatus.REJECTED:
                reason = fake.sentence(nb_words=6)

            existing_response = OrderResponse.query.filter_by(order_id=order.order_id, driver_id=driver.driver_id).first()
            if existing_response:
                logger.info(f"OrderResponse already exists for order_id={order.order_id} and driver_id={driver.driver_id}")
                continue

            response = OrderResponse(
                order_id=order.order_id,
                driver_id=driver.driver_id,
                status=status,
                reason=reason,
                responded_at=datetime.utcnow()
            )
            db.session.add(response)

        db.session.commit()
        logger.info(f"Seeded {num_entries} order responses successfully.")

def main():
    logger.info("Starting order responses seeding...")
    seed_order_responses()
    logger.info("Order responses seeding completed.")

if __name__ == "__main__":
    main()

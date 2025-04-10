from src.Models.orders import Order
from src.startup.database import db
from src.utils.logger import logger

def create_order(data):
    try:
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        logger.info(f"Order created with ID: {order.id}")
        return order
    except Exception as e:
        logger.error(f"Failed to create order: {str(e)}")
        db.session.rollback()
        raise

def get_all_orders(include_deleted=False):
    try:
        query = Order.query
        if not include_deleted and hasattr(Order, "is_deleted"):
            query = query.filter_by(is_deleted=False)
        return query.all()
    except Exception as e:
        logger.error(f"Error retrieving orders: {str(e)}")
        raise

def get_order_by_id(order_id):
    try:
        order = Order.query.get(order_id)
        if order and hasattr(order, "is_deleted") and order.is_deleted:
            return None
        return order
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {str(e)}")
        raise

def update_order(order_id, data):
    try:
        order = get_order_by_id(order_id)
        if not order:
            logger.warning(f"Update failed. Order {order_id} not found.")
            return None

        for key, value in data.items():
            if hasattr(order, key):
                setattr(order, key, value)

        db.session.commit()
        logger.info(f"Order {order.id} updated successfully.")
        return order
    except Exception as e:
        logger.error(f"Failed to update order {order_id}: {str(e)}")
        db.session.rollback()
        raise

def assign_driver_to_order(order_id, driver_id):
    try:
        order = get_order_by_id(order_id)
        if not order:
            logger.warning(f"Assignment failed. Order {order_id} not found.")
            return None

        order.driver_id = driver_id
        db.session.commit()
        logger.info(f"Driver {driver_id} assigned to Order {order_id}")
        return order
    except Exception as e:
        logger.error(f"Failed to assign driver to order {order_id}: {str(e)}")
        db.session.rollback()
        raise

def soft_delete_order(order_id):
    try:
        order = get_order_by_id(order_id)
        if not order:
            logger.warning(f"Delete failed. Order {order_id} not found.")
            return None

        if hasattr(order, "is_deleted"):
            order.is_deleted = True
            db.session.commit()
            logger.info(f"Order {order.id} soft deleted.")
            return order
        else:
            logger.error("Order model does not support soft deletion.")
            return None
    except Exception as e:
        logger.error(f"Failed to delete order {order_id}: {str(e)}")
        db.session.rollback()
        raise

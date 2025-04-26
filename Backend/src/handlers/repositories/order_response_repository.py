from src.Models.orderResponse import OrderResponse
from src.startup.database import db
from src.utils.logger import logger

def create_order_response(data):
    try:
        order_response = OrderResponse(**data)
        db.session.add(order_response)
        db.session.commit()
        logger.info(f"Order response created with ID: {order_response.response_id}")
        return order_response
    except Exception as e:
        logger.error(f"Failed to create order response: {str(e)}")
        db.session.rollback()
        raise

def get_all_order_responses():
    try:
        return OrderResponse.query.all()
    except Exception as e:
        logger.error(f"Error retrieving order responses: {str(e)}")
        raise

def get_order_response_by_id(order_response_id):
    try:
        return OrderResponse.query.get(order_response_id)
    except Exception as e:
        logger.error(f"Error retrieving order response {order_response_id}: {str(e)}")
        raise

def update_order_response(order_response_id, data):
    try:
        order_response = get_order_response_by_id(order_response_id)
        if not order_response:
            logger.warning(f"Update failed. Order response {order_response_id} not found.")
            return None

        for key, value in data.items():
            if hasattr(order_response, key):
                setattr(order_response, key, value)

        db.session.commit()
        logger.info(f"Order response {order_response.response_id} updated successfully.")
        return order_response
    except Exception as e:
        logger.error(f"Failed to update order response {order_response_id}: {str(e)}")
        db.session.rollback()
        raise

def delete_order_response(order_response_id):
    try:
        order_response = get_order_response_by_id(order_response_id)
        if not order_response:
            logger.warning(f"Delete failed. Order response {order_response_id} not found.")
            return None

        db.session.delete(order_response)
        db.session.commit()
        logger.info(f"Order response {order_response.response_id} deleted successfully.")
        return order_response
    except Exception as e:
        logger.error(f"Failed to delete order response {order_response_id}: {str(e)}")
        db.session.rollback()
        raise
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.order_repository import (
    create_order, get_all_orders, get_order_by_id,
    update_order, assign_driver_to_order
)
from src.decorators.permissions import role_required
from src.utils.logger import logger
from src.handlers.services.notification_service import NotificationService
from src.services.driver_assignment_service import DriverAssignmentService
from src.startup.database import db

@jwt_required()
@role_required(['admin', 'employee', 'user', 'manager'])
def create_order_view():
    
    data = request.get_json()
    try:
        order = create_order(data)
        logger.info(f"Order created: ID {order.id}")
        return jsonify(order.to_dict()), 201
    except ValueError as e:
        logger.warning(f"Order creation failed: {str(e)}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error creating order: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'employee', 'driver', 'user', 'manager'])
def get_orders_view():
    
    try:
        orders = get_all_orders()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'employee', 'driver', 'user', 'manager'])
def get_order_view(order_id):
   
    try:
        order = get_order_by_id(order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        return jsonify(order.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'employee', 'user', 'manager'])
def update_order_view(order_id):
   
    data = request.get_json()
    try:
        order = update_order(order_id, data)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        logger.info(f"Order {order.id} updated.")
        return jsonify(order.to_dict()), 200
    except Exception as e:
        logger.error(f"Error updating order {order_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def assign_driver_view(order_id):
    try:
        driver_assignment_service = DriverAssignmentService()
        result, status_code = driver_assignment_service.assign_driver_to_order(order_id)
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error assigning driver to order {order_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

def get_order_by_id(order_id):
    try:
        return Order.query.filter_by(order_id=order_id).first()
    except Exception as e:
        logger.error(f"Error fetching order by ID {order_id}: {str(e)}")
        raise

def update_order(order_id, data):
    try:
        order = get_order_by_id(order_id)
        if not order:
            return None
        for key, value in data.items():
            setattr(order, key, value)
        db.session.commit()
        return order
    except Exception as e:
        logger.error(f"Error updating order {order_id}: {str(e)}")
        db.session.rollback()
        raise

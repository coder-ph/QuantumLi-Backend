from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.order_repository import (
    create_order, get_all_orders, get_order_by_id,
    update_order, assign_driver_to_order
)
from src.decorators.permissions import role_required
from src.utils.logger import logger
@jwt_required()
@role_required(['admin', 'employee', 'user', 'manager'])
def create_order_view():
    """Create a new order"""
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
    """Get all orders"""
    try:
        orders = get_all_orders()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'employee', 'driver', 'user', 'manager'])
def get_order_view(order_id):
    """Get an order by ID"""
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
    """Update an existing order"""
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
    """Assign a driver to an order"""
    try:
        data = request.get_json()
        driver_id = data.get("driver_id")
        if not driver_id:
            return jsonify({"message": "Driver ID is required"}), 400

        order = assign_driver_to_order(order_id, driver_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404

        logger.info(f"Driver {driver_id} assigned to order {order.id}")
        return jsonify(order.to_dict()), 200
    except Exception as e:
        logger.error(f"Error assigning driver to order {order_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

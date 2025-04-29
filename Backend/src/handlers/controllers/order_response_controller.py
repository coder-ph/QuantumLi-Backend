from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.order_response_repository import (
    create_order_response, get_all_order_responses, get_order_response_by_id,
    update_order_response, delete_order_response
)
from src.decorators.permissions import role_required
from src.utils.logger import logger

@jwt_required()
@role_required([ 'admin', 'manager'])   
def create_order_response_view():
    data = request.get_json()
    try:
        order_response = create_order_response(data)
        logger.info(f"Order response created: ID {order_response.response_id}")
        return jsonify(order_response.to_dict()), 201
    except ValueError as e:
        logger.warning(f"Order response creation failed: {str(e)}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error creating order response: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin' , 'user' , 'manager', 'driver'])
def get_order_responses_view():
    try:
        order_responses = get_all_order_responses()
        return jsonify([response.to_dict() for response in order_responses]), 200
    except Exception as e:
        logger.error(f"Error fetching order responses: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'user', 'manager', 'driver'])
def get_order_response_view(response_id):
    try:
        order_response = get_order_response_by_id(response_id)
        if not order_response:
            return jsonify({"message": "Order response not found"}), 404
        return jsonify(order_response.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching order response {response_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def update_order_response_view(response_id):
    data = request.get_json()
    try:
        order_response = update_order_response(response_id, data)
        if not order_response:
            return jsonify({"message": "Order response not found"}), 404
        logger.info(f"Order response {order_response.response_id} updated.")
        return jsonify(order_response.to_dict()), 200
    except Exception as e:
        logger.error(f"Error updating order response {response_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def delete_order_response_view(response_id):
    try:
        order_response = delete_order_response(response_id)
        if not order_response:
            return jsonify({"message": "Order response not found"}), 404
        logger.info(f"Order response {order_response.response_id} deleted.")
        return jsonify({"message": "Order response deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting order response {response_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500
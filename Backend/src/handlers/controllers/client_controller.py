from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.handlers.repositories.client_repository import (
    create_client, get_all_clients, get_client_by_id,
    update_client, delete_client
)
from src.decorators.permissions import role_required
from src.utils.logger import logger

@jwt_required()
@role_required(['admin', 'manager'])
def create_client_view():
    data = request.get_json()
    try:
        client = create_client(data)
        logger.info(f"Client created: ID {client.get('id')}")
        return jsonify(client), 201
    except ValueError as e:
        logger.warning(f"Client creation failed: {str(e)}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error creating client: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def get_clients_view():
    try:
        clients = get_all_clients()
        return jsonify(clients if clients else []), 200
    except Exception as e:
        logger.error(f"Error fetching clients: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def get_client_view(client_id):
    try:
        client = get_client_by_id(client_id)
        if not client:
            return jsonify({"message": "Client not found"}), 404
        return jsonify(client), 200
    except Exception as e:
        logger.error(f"Error fetching client {client_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def update_client_view(client_id):
    data = request.get_json()
    try:
        client = update_client(client_id, data)
        if not client:
            return jsonify({"message": "Client not found"}), 404
        logger.info(f"Client {client_id} updated.")
        return jsonify(client), 200
    except Exception as e:
        logger.error(f"Error updating client {client_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def delete_client_view(client_id):
    try:
        client = delete_client(client_id)
        if not client:
            return jsonify({"message": "Client not found"}), 404
        logger.info(f"Client {client_id} deleted.")
        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting client {client_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

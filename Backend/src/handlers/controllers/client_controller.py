from flask import request, jsonify
from src.handlers.repositories import (
    create_client, get_all_clients, get_client_by_id, 
    update_client, delete_client
)
from functools import wraps
from flask_login import current_user
from src.utils.logger import logger
from src.error.apiErrors import NotFoundError, BadRequestError, UnauthorizedError

def is_authorized(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                logger.warning(f"Unauthorized access attempt by user {current_user.email} with role '{current_user.role}'")
                raise UnauthorizedError("Access denied: insufficient privileges.")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def response_handler(data=None, message=None, status=200):
    res = {}
    if message:
        res['message'] = message
    if data:
        res['data'] = data
    return jsonify(res), status

@is_authorized(['admin', 'manager'])
def create_client_view():
    try:
        data = request.get_json()
        if not data:
            raise BadRequestError("No input data provided.")
        client = create_client(data)
        logger.info(f"Client created: {client.get('id')}")
        return response_handler(client, "Client created successfully.", 201)
    except (BadRequestError, ValueError) as e:
        logger.error(f"Error creating client: {str(e)}")
        return response_handler(message=str(e), status=400)
    except Exception as e:
        logger.exception("Unexpected error during client creation")
        return response_handler(message="Server error", status=500)

@is_authorized(['admin', 'manager'])
def get_clients_view():
    try:
        clients = get_all_clients()
        if not clients:
            return response_handler(message="No clients found.", status=404)
        return response_handler(data=clients)
    except Exception as e:
        logger.exception("Failed to retrieve clients")
        return response_handler(message="Server error", status=500)

@is_authorized(['admin', 'manager'])
def get_client_view(client_id):
    try:
        client = get_client_by_id(client_id)
        if not client:
            raise NotFoundError("Client not found.")
        return response_handler(data=client)
    except NotFoundError as e:
        logger.warning(f"Client not found: {client_id}")
        return response_handler(message=str(e), status=404)
    except Exception as e:
        logger.exception("Error retrieving client")
        return response_handler(message="Server error", status=500)

@is_authorized(['admin', 'manager'])
def update_client_view(client_id):
    try:
        data = request.get_json()
        if not data:
            raise BadRequestError("No input data provided.")
        client = update_client(client_id, data)
        if not client:
            raise NotFoundError("Client not found.")
        logger.info(f"Client updated: {client_id}")
        return response_handler(data=client, message="Client updated successfully.")
    except (BadRequestError, ValueError) as e:
        logger.error(f"Validation error: {str(e)}")
        return response_handler(message=str(e), status=400)
    except NotFoundError as e:
        logger.warning(str(e))
        return response_handler(message=str(e), status=404)
    except Exception as e:
        logger.exception("Unexpected error during client update")
        return response_handler(message="Server error", status=500)

@is_authorized(['admin', 'manager'])
def delete_client_view(client_id):
    try:
        client = delete_client(client_id)
        if not client:
            raise NotFoundError("Client not found.")
        logger.info(f"Client deleted: {client_id}")
        return response_handler(message="Client deleted successfully.")
    except NotFoundError as e:
        logger.warning(str(e))
        return response_handler(message=str(e), status=404)
    except Exception as e:
        logger.exception("Unexpected error during client deletion")
        return response_handler(message="Server error", status=500)

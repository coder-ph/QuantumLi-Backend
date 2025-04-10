from src.Models.client import Client
from src.startup.database import db
from src.error.apiErrors import NotFoundError, BadRequestError
from src.utils.logger import logger

def create_client(data):
    try:
        client = Client(**data)
        db.session.add(client)
        db.session.commit()
        logger.info(f"New client created: {client.id}")
        return client.to_dict()
    except Exception as e:
        db.session.rollback()
        logger.exception("Failed to create client")
        raise BadRequestError("Could not create client.")

def get_all_clients():
    try:
        clients = Client.query.filter_by(is_deleted=False).all()
        return [client.to_dict() for client in clients]
    except Exception as e:
        logger.exception("Error retrieving all clients")
        raise

def get_client_by_id(client_id):
    try:
        client = Client.query.filter_by(id=client_id, is_deleted=False).first()
        if not client:
            raise NotFoundError("Client not found.")
        return client.to_dict()
    except NotFoundError as e:
        raise
    except Exception as e:
        logger.exception(f"Error fetching client by ID: {client_id}")
        raise

def update_client(client_id, data):
    try:
        client = Client.query.filter_by(id=client_id, is_deleted=False).first()
        if not client:
            raise NotFoundError("Client not found.")

        immutable_fields = ['id', 'created_at']
        for key, value in data.items():
            if key not in immutable_fields and hasattr(client, key):
                setattr(client, key, value)

        db.session.commit()
        logger.info(f"Client updated: {client.id}")
        return client.to_dict()
    except NotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        logger.exception("Failed to update client")
        raise BadRequestError("Could not update client.")

def delete_client(client_id):
    try:
        client = Client.query.filter_by(id=client_id, is_deleted=False).first()
        if not client:
            raise NotFoundError("Client not found.")

        client.is_deleted = True
        db.session.commit()
        logger.info(f"Client soft-deleted: {client.id}")
        return client.to_dict()
    except NotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        logger.exception("Failed to delete client")
        raise BadRequestError("Could not delete client.")

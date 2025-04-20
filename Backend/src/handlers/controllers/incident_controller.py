from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.incident_repository import IncidentRepository
from src.services.auth_service import get_current_user
from src.error.apiErrors import UnauthorizedError, NotFoundError, BadRequestError
from src.utils.logger import logger

incident_repo = IncidentRepository()

def is_authorized(user, allowed_roles):
 
    if user.role not in allowed_roles:
        logger.warning(f"Unauthorized access attempt by user {user.email} with role {user.role}")
        raise UnauthorizedError(f"Role '{user.role}' not permitted for this action.")

def validate_request_data(data):
  
    if not data.get("incident_type") or not data.get("description"):
        raise BadRequestError("Missing required fields: incident_type and description.")

@jwt_required()
def create_incident():
   
    user = get_current_user()
    data = request.get_json()

    try:
        validate_request_data(data)
        incident = incident_repo.create(data, user)
        logger.info(f"Incident created by {user.email}: {incident.incident_id}")
        return jsonify({'message': 'Incident created successfully.', 'incident_id': str(incident.incident_id)}), 201
    except BadRequestError as e:
        logger.error(f"Bad request when creating incident: {str(e)}")
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating incident: {str(e)}")
        return jsonify({'message': 'Failed to create incident.'}), 500

@jwt_required()
def get_all_incidents():

    user = get_current_user()
   
    incidents = incident_repo.get_all()
    if not incidents:
        logger.warning("No incidents found.")
        return jsonify({'message': 'No incidents found.'}), 404
    return jsonify([incident.to_dict() for incident in incidents]), 200

@jwt_required()
def get_incident(incident_id):
    
    user = get_current_user()
    incident = incident_repo.get_by_id(incident_id)
    if not incident:
        logger.warning(f"Incident with ID {incident_id} not found.")
        raise NotFoundError("Incident not found.")
    return jsonify(incident.to_dict()), 200

@jwt_required()
def delete_incident(incident_id):
   
    user = get_current_user()
    is_authorized(user, ['admin'])

    incident = incident_repo.get_by_id(incident_id)
    if not incident:
        logger.warning(f"Incident with ID {incident_id} not found for deletion.")
        raise NotFoundError("Incident not found.")

    incident_repo.delete(incident)
    logger.info(f"User {user.email} deleted incident: {incident.incident_id}")
    return jsonify({'message': 'Incident deleted successfully.'}), 200

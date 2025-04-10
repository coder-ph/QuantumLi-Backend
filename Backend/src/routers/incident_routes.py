from flask import Blueprint
from src.handlers.controllers.incident_controller import (
    create_incident,
    get_all_incidents,
    get_incident,
    delete_incident
)

incidents_bp = Blueprint('incidents_bp', __name__)

incidents_bp.route('/incidents', methods=['POST'])(create_incident)
incidents_bp.route('/incidents', methods=['GET'])(get_all_incidents)
incidents_bp.route('/incidents/<uuid:incident_id>', methods=['GET'])(get_incident)
incidents_bp.route('/incidents/<uuid:incident_id>', methods=['DELETE'])(delete_incident)

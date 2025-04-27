from flask import Blueprint
from src.handlers.controllers.driver_controller import (
    create_driver_view,
    get_all_drivers_view,
    get_driver_view,
    update_driver_view,
    delete_driver_view,
    upload_document_view,
    update_document_status_view,
    get_documents_view
)

drivers_bp = Blueprint('drivers_bp', __name__)

drivers_bp.route('/drivers', methods=['POST'])(create_driver_view)
drivers_bp.route('/drivers', methods=['GET'])(get_all_drivers_view)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['GET'])(get_driver_view)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['PUT'])(update_driver_view)
drivers_bp.route('/drivers/<uuid:driver_id>', methods=['DELETE'])(delete_driver_view)


drivers_bp.route('/drivers/<uuid:driver_id>/documents', methods=['POST'])(upload_document_view)
drivers_bp.route('/drivers/<uuid:driver_id>/documents', methods=['GET'])(get_documents_view)
drivers_bp.route('/documents/<uuid:document_id>/status', methods=['PUT'])(update_document_status_view)

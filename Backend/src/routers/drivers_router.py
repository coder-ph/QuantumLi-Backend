from flask import Blueprint
from src.handlers.controllers.driver_controller import (
    create_driver_view,
    get_all_drivers_view,
    get_driver_view,
    update_driver_view,
    delete_driver_view,
    upload_document_view,
    update_document_status_view,
    get_documents_view,
    # create_driver_location_view,
    # get_all_driver_location_view,
    # get_driver_location_by_id_view,
    # update_driver_location_view,
    update_driver_status_view,
    create_driver_status_view,
    get_all_drivers_statuses_view,
    get_driver_status_by_id_view,
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

# drivers_bp.route('/drivers/location', methods=['POST'])(create_driver_location_view)
# drivers_bp.route('/drivers/location', methods=['GET'])(get_all_driver_location_view)
# drivers_bp.route('/drivers/location/<uuid:driver_id>', methods=['GET'])(get_driver_location_by_id_view)
# drivers_bp.route('/drivers/location/<uuid:driver_id>',methods=['PUT'])(update_driver_location_view)

drivers_bp.route('/drivers/status', methods=['POST'])(create_driver_status_view)
drivers_bp.route('/drivers/status', methods=['GET'])(get_all_drivers_statuses_view)
drivers_bp.route('/drivers/status/<uuid:driver_id>', methods=['GET'])(get_driver_status_by_id_view)
drivers_bp.route('/drivers/status/<uuid:driver_id>',methods=['PUT'])(update_driver_status_view)

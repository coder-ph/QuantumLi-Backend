from flask import Blueprint
from src.handlers.controllers.client_controller import create_client_view, get_clients_view, get_client_view, update_client_view, delete_client_view

client_bp = Blueprint('client_bp', __name__)

client_bp.route('/clients', methods=['POST'])(create_client_view)
client_bp.route('/clients', methods=['GET'])(get_clients_view)
client_bp.route('/clients/<uuid:client_id>', methods=['GET'])(get_client_view)
client_bp.route('/clients/<uuid:client_id>', methods=['PUT'])(update_client_view)
client_bp.route('/clients/<uuid:client_id>', methods=['DELETE'])(delete_client_view)

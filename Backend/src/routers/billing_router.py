from flask import Blueprint
from src.handlers.controllers.billing_controller import (
    create_invoice,
    get_all_invoices,
    get_invoice,
    update_invoice,
    delete_invoice,
    restore_invoice
)

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

billing_bp.route('/', methods=['POST'])(create_invoice)
billing_bp.route('/', methods=['GET'])(get_all_invoices)
billing_bp.route('/<uuid:invoice_id>', methods=['GET'])(get_invoice)
billing_bp.route('/<uuid:invoice_id>', methods=['PUT'])(update_invoice)
billing_bp.route('/<uuid:invoice_id>', methods=['DELETE'])(delete_invoice)
billing_bp.route('/<uuid:invoice_id>/restore', methods=['PUT'])(restore_invoice)

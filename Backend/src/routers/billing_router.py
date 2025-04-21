from flask import Blueprint
from src.handlers.controllers.billing_controller import (
    create_invoice_view,
    get_all_invoices_view,
    get_invoice_view,
    update_invoice_view,
    delete_invoice_view,
    restore_invoice_view
 
)

billing_bp = Blueprint('billing', __name__)

billing_bp.route('/billing', methods=['POST'])(create_invoice_view)
billing_bp.route('/billing', methods=['GET'])(get_all_invoices_view)
billing_bp.route('/billing/<uuid:invoice_id>', methods=['GET'])(get_invoice_view)
billing_bp.route('/billing/<uuid:invoice_id>', methods=['PUT'])(update_invoice_view)
billing_bp.route('/billing/<uuid:invoice_id>', methods=['DELETE'])(delete_invoice_view)
billing_bp.route('/billing/<uuid:invoice_id>/restore', methods=['PUT'])(restore_invoice_view)

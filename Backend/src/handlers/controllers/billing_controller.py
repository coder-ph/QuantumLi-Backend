from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.handlers.repositories.billing_repository import BillingRepository
from src.schemas.billing_schema import BillingSchema
from src.decorators.permissions import role_required
from src.utils.logger import logger

billing_repo = BillingRepository()
billing_schema = BillingSchema()
billings_schema = BillingSchema(many=True)

@jwt_required()
@role_required(['admin', 'manager'])
def create_invoice_view():
    data = request.get_json()
    try:
        errors = billing_schema.validate(data)
        if errors:
            logger.warning(f"Validation errors: {errors}")
            return jsonify({"message": "Validation failed", "errors": errors}), 400

        invoice = billing_repo.create(data)
        if not invoice:
            return jsonify({"message": "Failed to create invoice."}), 400

        logger.info(f"Invoice created: ID {invoice.invoice_id}")
        return jsonify({
            'message': 'Billing invoice created successfully.',
            'invoice_id': str(invoice.invoice_id)
        }), 201
    except Exception as e:
        logger.error(f"Unexpected error creating invoice: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager', 'employee'])
def get_all_invoices_view():
    try:
        invoices = billing_repo.get_all()
        return jsonify(billings_schema.dump(invoices)), 200
    except Exception as e:
        logger.error(f"Error fetching invoices: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager', 'employee'])
def get_invoice_view(invoice_id):
    try:
        invoice = billing_repo.get_by_id(invoice_id)
        if not invoice:
            return jsonify({"message": "Invoice not found"}), 404
        return jsonify(billing_schema.dump(invoice)), 200
    except Exception as e:
        logger.error(f"Error fetching invoice {invoice_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def update_invoice_view(invoice_id):
    data = request.get_json()
    try:
        invoice = billing_repo.get_by_id(invoice_id)
        if not invoice:
            return jsonify({"message": "Invoice not found"}), 404

        errors = billing_schema.validate(data, partial=True)
        if errors:
            logger.warning(f"Validation errors on update: {errors}")
            return jsonify({"message": "Validation failed", "errors": errors}), 400

        updated_invoice = billing_repo.update(invoice, data)
        if not updated_invoice:
            return jsonify({"message": "Failed to update invoice."}), 400

        logger.info(f"Invoice {invoice_id} updated.")
        return jsonify(billing_schema.dump(updated_invoice)), 200
    except Exception as e:
        logger.error(f"Error updating invoice {invoice_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def delete_invoice_view(invoice_id):
    try:
        invoice = billing_repo.get_by_id(invoice_id)
        if not invoice:
            return jsonify({"message": "Invoice not found"}), 404

        if invoice.is_deleted:
            return jsonify({"message": "Invoice already deleted."}), 400

        billing_repo.delete(invoice)
        logger.info(f"Invoice {invoice_id} soft-deleted.")
        return jsonify({"message": "Billing invoice deleted successfully."}), 200
    except Exception as e:
        logger.error(f"Error deleting invoice {invoice_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
def restore_invoice_view(invoice_id):
    try:
        invoice = billing_repo.get_by_id(invoice_id)
        if not invoice:
            return jsonify({"message": "Invoice not found"}), 404

        if not invoice.is_deleted:
            return jsonify({"message": "Invoice is already active."}), 200

        billing_repo.restore(invoice)
        logger.info(f"Invoice {invoice_id} restored.")
        return jsonify({"message": "Billing invoice restored successfully."}), 200
    except Exception as e:
        logger.error(f"Error restoring invoice {invoice_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

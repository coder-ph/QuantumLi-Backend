from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.billing_repository import BillingRepository
from src.schemas.billing_schema import BillingSchema
from src.services.auth_service import get_current_user
from src.error.apiErrors import UnauthorizedError, NotFoundError, BadRequestError
from src.utils.logger import logger

billing_repo = BillingRepository()
billing_schema = BillingSchema()
billings_schema = BillingSchema(many=True)

def is_authorized(user, allowed_roles):
    if user.role not in allowed_roles:
        raise UnauthorizedError(f"Role '{user.role}' not permitted for this action.")

@jwt_required()
def create_invoice():
    user = get_current_user()
    is_authorized(user, ['admin', 'manager'])

    data = request.get_json()
    errors = billing_schema.validate(data)
    if errors:
        logger.warning(f"Validation errors in create_invoice: {errors}")
        raise BadRequestError(errors)

    billing = billing_repo.create(data)
    if not billing:
        raise BadRequestError("Failed to create invoice.")

    logger.info(f"User {user.email} created invoice {billing.invoice_id}")
    return jsonify({
        'message': 'Billing invoice created successfully.',
        'invoice_id': str(billing.invoice_id)
    }), 201

@jwt_required()
def get_all_invoices():
    user = get_current_user()
    is_authorized(user, ['admin', 'manager', 'employee'])

    invoices = billing_repo.get_all()
    logger.info(f"User {user.email} fetched {len(invoices)} invoices.")
    return jsonify(billings_schema.dump(invoices)), 200

@jwt_required()
def get_invoice(invoice_id):
    user = get_current_user()
    is_authorized(user, ['admin', 'manager', 'employee'])

    invoice = billing_repo.get_by_id(invoice_id)
    if not invoice:
        logger.warning(f"Invoice {invoice_id} not found for user {user.email}")
        raise NotFoundError("Invoice not found.")

    logger.info(f"User {user.email} fetched invoice {invoice_id}")
    return jsonify(billing_schema.dump(invoice)), 200

@jwt_required()
def update_invoice(invoice_id):
    user = get_current_user()
    is_authorized(user, ['admin', 'manager'])

    invoice = billing_repo.get_by_id(invoice_id)
    if not invoice:
        logger.warning(f"Invoice {invoice_id} not found for update by {user.email}")
        raise NotFoundError("Invoice not found.")

    update_data = request.get_json()
    errors = billing_schema.validate(update_data, partial=True)
    if errors:
        logger.warning(f"Validation errors during update_invoice: {errors}")
        raise BadRequestError(errors)

    updated_invoice = billing_repo.update(invoice, update_data)
    if not updated_invoice:
        raise BadRequestError("Failed to update invoice.")

    logger.info(f"User {user.email} updated invoice {invoice_id}")
    return jsonify({
        'message': 'Invoice updated successfully.',
        'invoice': billing_schema.dump(updated_invoice)
    }), 200
    
@jwt_required()
def delete_invoice(invoice_id):
    user = get_current_user()
    is_authorized(user, ['admin', 'manager'])

    
    invoice = billing_repo.get_by_id(invoice_id)
    if not invoice:
        logger.warning(f"Invoice {invoice_id} not found for deletion by {user.email}")
        raise NotFoundError("Invoice not found.")

    if invoice.is_deleted:
        logger.warning(f"Invoice {invoice_id} already deleted.")
        raise BadRequestError("Invoice already deleted.")

    try:
        billing_repo.delete(invoice)
        logger.info(f"User {user.email} soft-deleted invoice {invoice_id}")
        return jsonify({'message': 'Billing invoice deleted successfully.'}), 200
    except Exception as e:
        logger.error(f"Error deleting invoice {invoice_id}: {str(e)}")
        raise BadRequestError("Failed to delete invoice.")

@jwt_required()
def restore_invoice(invoice_id):
    user = get_current_user()
    is_authorized(user, ['admin', 'manager'])
    
    invoice = billing_repo.get_by_id(invoice_id)
    if not invoice:
        logger.warning(f"Invoice {invoice_id} not found for restoration by {user.email}")
        raise NotFoundError("Invoice not found.")

    if not invoice.is_deleted:
        logger.info(f"Invoice {invoice_id} is already active, skipping restore.")
        return jsonify({'message': 'Invoice is already active.'}), 200

    try:
        billing_repo.restore(invoice)
        logger.info(f"User {user.email} restored invoice {invoice_id}")
        return jsonify({'message': 'Billing invoice restored successfully.'}), 200
    except Exception as e:
        logger.error(f"Error restoring invoice {invoice_id}: {str(e)}")
        raise BadRequestError("Failed to restore invoice.")

from marshmallow import Schema, fields, validate

class BillingSchema(Schema):
    invoice_id = fields.UUID(dump_only=True, description="Unique ID of the invoice")
    client_id = fields.UUID(required=True, description="ID of the client associated with the invoice")
    
    invoice_date = fields.Date(
        missing=None,
        allow_none=True,
        description="Date when the invoice was generated"
    )
    
    due_date = fields.Date(
        required=True,
        description="Deadline for invoice payment"
    )
    
    total_amount = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        description="Total amount including tax"
    )
    
    tax_amount = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        description="Tax portion of the total amount"
    )
    
    status = fields.Str(
        validate=validate.OneOf(["unpaid", "paid", "overdue", "cancelled"]),
        missing="unpaid",
        description="Current status of the invoice"
    )
    
    payment_date = fields.Date(
        allow_none=True,
        missing=None,
        description="Date when the payment was made"
    )
    
    payment_method = fields.Str(
        validate=validate.OneOf(["cash", "mpesa", "bank_transfer", "card", "paypal"]),
        allow_none=True,
        missing=None,
        description="Method used for payment"
    )
    
    reference_numbers = fields.Str(
        allow_none=True,
        missing=None,
        description="Transaction reference numbers or receipts"
    )
    
    notes = fields.Str(
        allow_none=True,
        missing=None,
        description="Additional notes or metadata"
    )
    
    is_deleted = fields.Bool(
        dump_only=True,
        description="Flag indicating if the record is soft-deleted"
    )
    
    created_at = fields.DateTime(
        dump_only=True,
        description="Timestamp of invoice creation"
    )
    
    updated_at = fields.DateTime(
        dump_only=True,
        description="Timestamp of the last update"
    )

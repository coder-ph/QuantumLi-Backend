from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class DriverSchema(Schema):
    driver_id = fields.UUID(dump_only=True)
    carrier_id = fields.UUID(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    license_number = fields.Str(required=True, validate=validate.Length(min=5))
    license_type = fields.Str(required=True)
    license_expiry = fields.Date(required=True)
    contact_phone = fields.Str(required=True, validate=validate.Regexp(r'^\+?[0-9]{9,15}$'))
    email = fields.Email(required=True)
    address = fields.Str(required=True)
    emergency_contact = fields.Str(required=True)
    medical_certificate_expiry = fields.Date(required=True)
    training_certifications = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'inactive']))
    is_deleted = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('license_expiry')
    def validate_license_expiry(self, value):
        if value < datetime.utcnow().date():
            raise ValidationError("License expiry date cannot be in the past.")

    @validates('medical_certificate_expiry')
    def validate_med_cert_expiry(self, value):
        if value < datetime.utcnow().date():
            raise ValidationError("Medical certificate expiry cannot be in the past.")

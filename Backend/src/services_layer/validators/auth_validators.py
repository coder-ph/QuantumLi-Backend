from marshmallow import Schema, fields, validate, ValidationError, validates
from src.utils.logger import logger  

ALLOWED_ROLES = ["admin", "manager", "driver", "client", "user"]

class SignUpSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Enter a valid email address."
        },
        validate=validate.Length(max=255),
        description="User's email address"
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128),
        error_messages={
            "required": "Password is required.",
            "invalid": "Password must be at least 8 characters long."
        },
        description="Password (min 8 characters)"
    )

    username= fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={
            "required": "Full name is required.",
            "invalid": "Full name must be at least 2 characters long."
        },
        description="User's full name"
    )

    phone = fields.String(
        required=True,
        validate=validate.Length(min=10, max=13),
        error_messages={
            "required": "Phone number is required.",
            "invalid": "Invalid phone number format."
        },
        description="Phone number starting with 07 (10 digits) or +254 (13 characters)"
    )

    role = fields.String(
        required=False,
        validate=validate.OneOf(ALLOWED_ROLES),
        description="Optional user role (admin, manager, driver, client)"
    )

    @validates("phone")
    def validate_phone(self, value):
        """
        Custom validation for Kenyan phone numbers:
        - Must start with '07' and be 10 digits long
        - Or start with '+254' and be 13 characters long
        """
        if value.startswith("07") and len(value) == 10:
            return
        elif value.startswith("+254") and len(value) == 13:
            return
        else:
            logger.warning(f"Phone validation failed for value: {value}")
            raise ValidationError("Phone must start with '07' (10 digits) or '+254' (13 characters)")

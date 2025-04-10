from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.Models.systemusers import System_Users


class SystemUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = System_Users
        load_instance = True
        include_relationships = True
        exclude = ('password_hash', 'password_reset_token')

    # ID & timestamps
    user_id = fields.UUID(dump_only=True, description="Unique identifier for the user")
    created_at = fields.DateTime(dump_only=True, description="Account creation timestamp")
    updated_at = fields.DateTime(dump_only=True, description="Last update timestamp")

    # Basic fields
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        description="Username must be between 3 and 50 characters"
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=100),
        description="Valid email address"
    )
    phone = fields.Str(
        required=True,
        validate=validate.Regexp(r'^\+?[0-9]{10,13}$'),
        description="Phone number with optional '+' and 7-15 digits"
    )
    role = fields.Str(
        required=True,
        validate=validate.OneOf(["admin", "user", "manager", "auditor"]),  
        description="User role (admin, user, manager, etc.)"
    )

    last_login = fields.DateTime(dump_only=True, description="Last login timestamp")
    is_active = fields.Bool(description="Whether the user is active")
    status = fields.Str(
        validate=validate.OneOf(["active", "inactive", "suspended"]),
        description="Account status"
    )

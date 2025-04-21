from marshmallow import Schema, fields, validate, validates_schema, ValidationError, post_load
from src.utils.logger import logger



class ProductSchema(Schema):
  
    product_id = fields.UUID(dump_only=True)
    client_id = fields.UUID(required=True, error_messages={"required": "Client ID is required."})

  
    sku = fields.Str(
        required=True,
        validate=validate.Length(max=100),
        error_messages={"required": "SKU is required."}
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(max=200),
        error_messages={"required": "Product name is required."}
    )
    description = fields.Str(validate=validate.Length(max=500))
    category = fields.Str(validate=validate.Length(max=100))

    
    weight = fields.Float(validate=validate.Range(min=0, error="Weight must be a positive number."))
    dimensions = fields.Str(
        validate=validate.Regexp(
            r'^\d+x\d+x\d+$',
            error="Dimensions must follow the format 'LxWxH' using digits only (e.g., '10x20x15')."
        )
    )
    unit_volume = fields.Float(validate=validate.Range(min=0, error="Unit volume must be positive."))


    hazardous = fields.Bool()
    perishable = fields.Bool()
    temperature_requirements = fields.Str(validate=validate.Length(max=100))
    handling_requirements = fields.Str(validate=validate.Length(max=200))
    customs_tariff_code = fields.Str(validate=validate.Length(max=100))
    value = fields.Float(validate=validate.Range(min=0, error="Value must be a positive number."))

   
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_custom_rules(self, data, **kwargs):
        """
        Custom cross-field validation logic (optional).
        """
        if data.get("perishable") and not data.get("temperature_requirements"):
            error_msg = "Temperature requirements are required for perishable items."
            logger.warning(f"[Validation] {error_msg}")
            raise ValidationError({"temperature_requirements": error_msg})

    @post_load
    def log_valid_data(self, data, **kwargs):
        """
        Optional post-processing of data.
        You could, for example, clean strings or log successful validation.
        """
        logger.info(f"[ProductSchema] Validated product data: {data}")
        return data

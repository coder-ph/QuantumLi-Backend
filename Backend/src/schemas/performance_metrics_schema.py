from marshmallow import Schema, fields

class TimePeriodSchema(Schema):
    start_date = fields.Date(required=False, description="The start date for the time period filter.")
    end_date = fields.Date(required=False, description="The end date for the time period filter.")

class DeliveriesPerDriverRequestSchema(Schema):
    time_period = fields.Nested(TimePeriodSchema, required=False)
    delivery_count_threshold_min = fields.Int(required=False, description="Minimum number of deliveries for the filter.")
    delivery_count_threshold_max = fields.Int(required=False, description="Maximum number of deliveries for the filter.")

class AverageDeliveryTimeRequestSchema(Schema):
    time_period = fields.Nested(TimePeriodSchema, required=False)
    average_delivery_time_min = fields.Float(required=False, description="Minimum average delivery time for the filter.")
    average_delivery_time_max = fields.Float(required=False, description="Maximum average delivery time for the filter.")

class OrderAcceptanceRejectionRequestSchema(Schema):
    time_period = fields.Nested(TimePeriodSchema, required=False)
    order_rejection_rate_min = fields.Float(required=False, description="Minimum order rejection rate for the filter.")
    order_rejection_rate_max = fields.Float(required=False, description="Maximum order rejection rate for the filter.")

class CustomerRatingsRequestSchema(Schema):
    time_period = fields.Nested(TimePeriodSchema, required=False)
    customer_rating_threshold_min = fields.Float(required=False, description="Minimum customer rating for the filter.")
    customer_rating_threshold_max = fields.Float(required=False, description="Maximum customer rating for the filter.")

class DeliveriesPerDriverResponseSchema(Schema):
    driver_id = fields.UUID(description="Unique identifier for the driver.")
    delivery_count = fields.Int(description="Total number of deliveries made by the driver.")

class AverageDeliveryTimeResponseSchema(Schema):
    driver_id = fields.UUID(description="Unique identifier for the driver.")
    average_delivery_time = fields.Float(description="Average delivery time for the driver in minutes.")

class OrderAcceptanceRejectionResponseSchema(Schema):
    driver_id = fields.UUID(description="Unique identifier for the driver.")
    acceptance_rate = fields.Float(description="Percentage of accepted orders for the driver.")
    rejection_rate = fields.Float(description="Percentage of rejected orders for the driver.")

class CustomerRatingsResponseSchema(Schema):
    driver_id = fields.UUID(description="Unique identifier for the driver.")
    average_rating = fields.Float(description="Average customer rating for the driver.")

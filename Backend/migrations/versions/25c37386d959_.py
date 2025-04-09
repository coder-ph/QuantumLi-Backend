"""empty message

Revision ID: 25c37386d959
Revises: 
Create Date: 2025-04-09 00:19:03.428420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25c37386d959'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carriers',
    sa.Column('carrier_id', sa.UUID(), nullable=False),
    sa.Column('carrier_name', sa.String(length=255), nullable=False),
    sa.Column('carrier_type', sa.String(length=50), nullable=False),
    sa.Column('contact_person', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=False),
    sa.Column('account_number', sa.String(length=100), nullable=True),
    sa.Column('contract_details', sa.Text(), nullable=True),
    sa.Column('service_levels', sa.Text(), nullable=True),
    sa.Column('insurance_details', sa.Text(), nullable=True),
    sa.Column('performance_rating', sa.Float(), nullable=True),
    sa.CheckConstraint('performance_rating >= 0 AND performance_rating <= 5', name='check_performance_rating'),
    sa.PrimaryKeyConstraint('carrier_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('clients',
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('company_name', sa.String(length=100), nullable=False),
    sa.Column('contact_person', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=14), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('tax_id', sa.String(length=50), nullable=True),
    sa.Column('registration_number', sa.String(length=50), nullable=True),
    sa.Column('account_status', sa.Enum('active', 'inactive', name='account_status'), nullable=True),
    sa.Column('credit_limit', sa.Float(), nullable=True),
    sa.Column('payment_terms', sa.String(length=50), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('client_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email', name='uq_client_email'),
    sa.UniqueConstraint('registration_number', name='uq_client_registration_number'),
    sa.UniqueConstraint('tax_id', name='uq_client_tax_id')
    )
    op.create_table('employees',
    sa.Column('employee_id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('position', sa.String(length=100), nullable=False),
    sa.Column('department', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('hire_date', sa.DateTime(), nullable=False),
    sa.Column('termination_date', sa.DateTime(), nullable=True),
    sa.Column('supervisor_id', sa.UUID(), nullable=True),
    sa.Column('access_level', sa.String(length=50), nullable=False),
    sa.Column('login_credentials', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['supervisor_id'], ['employees.employee_id'], ),
    sa.PrimaryKeyConstraint('employee_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('incidents',
    sa.Column('incident_id', sa.UUID(), nullable=False),
    sa.Column('related_to', sa.Enum('shipment', 'order', name='related_to_enum'), nullable=False),
    sa.Column('related_id', sa.UUID(), nullable=False),
    sa.Column('incident_type', sa.Enum('damage', 'delay', 'loss', 'theft', name='incident_type_enum'), nullable=False),
    sa.Column('severity', sa.Enum('high', 'medium', 'low', name='severity_enum'), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('reported_by', sa.String(length=255), nullable=False),
    sa.Column('report_date', sa.Date(), nullable=False),
    sa.Column('resolution_status', sa.Enum('open', 'resolved', 'pending', name='resolution_status_enum'), nullable=False),
    sa.Column('resolution_details', sa.Text(), nullable=True),
    sa.Column('compensation_amount', sa.Float(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('incident_id')
    )
    op.create_table('locations',
    sa.Column('location_id', sa.UUID(), nullable=False),
    sa.Column('location_name', sa.String(length=100), nullable=False),
    sa.Column('location_type', sa.Enum('warehouse', 'hub', 'customer', 'other', name='location_type'), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state_province', sa.String(length=100), nullable=True),
    sa.Column('postal_code', sa.String(length=20), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('contact_person', sa.String(length=100), nullable=True),
    sa.Column('contact_phone', sa.String(length=15), nullable=True),
    sa.Column('operating_hours', sa.String(length=100), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('location_id'),
    sa.UniqueConstraint('address', name='uq_location_address')
    )
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.create_index('idx_location_city_country', ['city', 'country'], unique=False)
        batch_op.create_index('idx_location_type', ['location_type'], unique=False)

    op.create_table('notifications',
    sa.Column('notification_id', sa.UUID(), nullable=False),
    sa.Column('recipient_id', sa.UUID(), nullable=False),
    sa.Column('message', sa.String(length=500), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('status', sa.Enum('sent', 'read', 'unread', 'failed', name='notification_status'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('read_at', sa.DateTime(), nullable=True),
    sa.Column('related_entity', sa.String(length=100), nullable=True),
    sa.Column('related_id', sa.UUID(), nullable=True),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('third_party_services',
    sa.Column('service_id', sa.UUID(), nullable=False),
    sa.Column('service_name', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('contact_info', sa.String(length=150), nullable=True),
    sa.Column('authentication_method', sa.Enum('api_key', 'oauth2', 'basic_auth', 'jwt', name='authentication_method_enum'), nullable=False),
    sa.Column('config_details', sa.JSON(), nullable=False),
    sa.Column('active_status', sa.Boolean(), nullable=True),
    sa.Column('integration_logs', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('billing',
    sa.Column('invoice_id', sa.UUID(), nullable=False),
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('invoice_date', sa.Date(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('tax_amount', sa.Float(), nullable=False),
    sa.Column('status', sa.Enum('draft', 'paid', 'overdue', name='invoice_status'), nullable=False),
    sa.Column('payment_date', sa.Date(), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=True),
    sa.Column('reference_numbers', sa.String(length=100), nullable=True),
    sa.Column('notes', sa.String(length=255), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], ),
    sa.PrimaryKeyConstraint('invoice_id')
    )
    op.create_table('drivers',
    sa.Column('driver_id', sa.UUID(), nullable=False),
    sa.Column('carrier_id', sa.UUID(), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('license_number', sa.String(length=100), nullable=False),
    sa.Column('license_type', sa.String(length=50), nullable=False),
    sa.Column('license_expiry', sa.Date(), nullable=False),
    sa.Column('contact_phone', sa.String(length=15), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('emergency_contact', sa.String(length=255), nullable=True),
    sa.Column('medical_certificate_expiry', sa.Date(), nullable=False),
    sa.Column('training_certifications', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['carrier_id'], ['carriers.carrier_id'], ),
    sa.PrimaryKeyConstraint('driver_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('license_number')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('order_reference', sa.String(length=100), nullable=False),
    sa.Column('order_date', sa.Date(), nullable=False),
    sa.Column('requested_pickup_date', sa.Date(), nullable=False),
    sa.Column('requested_delivery_date', sa.Date(), nullable=False),
    sa.Column('priority', sa.String(length=50), nullable=False),
    sa.Column('special_instructions', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('DRAFT', 'CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'CANCELED', name='orderstatus'), nullable=False),
    sa.Column('billing_type', sa.Enum('PREPAID', 'COLLECT', 'THIRD_PARTY', name='billingtype'), nullable=False),
    sa.Column('payment_status', sa.Enum('PAID', 'UNPAID', 'PENDING', name='paymentstatus'), nullable=False),
    sa.Column('total_weight', sa.Float(), nullable=False),
    sa.Column('total_volume', sa.Float(), nullable=False),
    sa.Column('declared_value', sa.Float(), nullable=False),
    sa.Column('required_documents', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], ),
    sa.PrimaryKeyConstraint('order_id'),
    sa.UniqueConstraint('order_reference')
    )
    op.create_table('products',
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('sku', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('dimensions', sa.String(length=50), nullable=True),
    sa.Column('unit_volume', sa.Float(), nullable=True),
    sa.Column('hazardous', sa.Boolean(), nullable=True),
    sa.Column('perishable', sa.Boolean(), nullable=True),
    sa.Column('temperature_requirements', sa.String(length=100), nullable=True),
    sa.Column('handling_requirements', sa.String(length=200), nullable=True),
    sa.Column('customs_tariff_code', sa.String(length=100), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], ),
    sa.PrimaryKeyConstraint('product_id'),
    sa.UniqueConstraint('client_id', 'sku', name='uq_client_sku'),
    sa.UniqueConstraint('sku')
    )
    op.create_table('rates',
    sa.Column('rate_id', sa.UUID(), nullable=False),
    sa.Column('client_id', sa.UUID(), nullable=True),
    sa.Column('rate_name', sa.String(length=255), nullable=False),
    sa.Column('effective_date', sa.Date(), nullable=False),
    sa.Column('expiry_date', sa.Date(), nullable=True),
    sa.Column('service_type', sa.Enum('air', 'road', 'sea', 'rail', name='service_type_enum'), nullable=False),
    sa.Column('origin_zone', sa.String(length=255), nullable=False),
    sa.Column('destination_zone', sa.String(length=255), nullable=False),
    sa.Column('weight_break', sa.String(length=255), nullable=False),
    sa.Column('volume_break', sa.String(length=255), nullable=False),
    sa.Column('rate_per_unit', sa.Float(), nullable=False),
    sa.Column('minimum_charge', sa.Float(), nullable=False),
    sa.Column('accessorial_charges', sa.Float(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], ),
    sa.PrimaryKeyConstraint('rate_id')
    )
    op.create_table('system_users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('employee_id', sa.UUID(), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'employee', 'driver', 'user', 'manager', name='user_role_enum'), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('password_reset_token', sa.String(length=255), nullable=True),
    sa.Column('password_expiry', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('vehicles',
    sa.Column('vehicle_id', sa.UUID(), nullable=False),
    sa.Column('carrier_id', sa.UUID(), nullable=True),
    sa.Column('registration_number', sa.String(length=100), nullable=False),
    sa.Column('vehicle_type', sa.String(length=50), nullable=False),
    sa.Column('make', sa.String(length=100), nullable=False),
    sa.Column('model', sa.String(length=100), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('max_weight_capacity', sa.Float(), nullable=False),
    sa.Column('max_volume_capacity', sa.Float(), nullable=False),
    sa.Column('current_location_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('last_maintenance_date', sa.Date(), nullable=True),
    sa.Column('next_maintenance_date', sa.Date(), nullable=True),
    sa.Column('insurance_expiry', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['carrier_id'], ['carriers.carrier_id'], ),
    sa.ForeignKeyConstraint(['current_location_id'], ['locations.location_id'], ),
    sa.PrimaryKeyConstraint('vehicle_id'),
    sa.UniqueConstraint('registration_number')
    )
    op.create_table('warehouse_operations',
    sa.Column('operation_id', sa.UUID(), nullable=False),
    sa.Column('location_id', sa.UUID(), nullable=False),
    sa.Column('operation_type', sa.String(), nullable=False),
    sa.Column('reference_id', sa.UUID(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('operator_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('IN_PROGRESS', 'COMPLETED', 'PENDING', 'CANCELED', name='operationstatus'), nullable=False),
    sa.Column('equipment_used', sa.String(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['operator_id'], ['employees.employee_id'], ),
    sa.PrimaryKeyConstraint('operation_id')
    )
    op.create_table('audit_logs',
    sa.Column('log_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('action_type', sa.String(length=50), nullable=False),
    sa.Column('affected_table', sa.String(length=100), nullable=False),
    sa.Column('record_id', sa.UUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('ip_address', sa.String(length=45), nullable=False),
    sa.Column('user_agent', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['system_users.user_id'], ),
    sa.PrimaryKeyConstraint('log_id')
    )
    op.create_table('inventory',
    sa.Column('inventory_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('location_id', sa.UUID(), nullable=False),
    sa.Column('quantity_on_hand', sa.Integer(), nullable=False),
    sa.Column('quantity_allocated', sa.Integer(), nullable=False),
    sa.Column('quantity_on_order', sa.Integer(), nullable=False),
    sa.Column('last_stock_take_date', sa.Date(), nullable=True),
    sa.Column('bin_location', sa.String(length=100), nullable=True),
    sa.Column('batch_number', sa.String(length=100), nullable=True),
    sa.Column('expiry_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('inventory_id')
    )
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.create_index('idx_inventory_location_id', ['location_id'], unique=False)
        batch_op.create_index('idx_inventory_product_id', ['product_id'], unique=False)

    op.create_table('inventory_movements',
    sa.Column('movement_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('from_location_id', sa.UUID(), nullable=False),
    sa.Column('to_location_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('movement_type', sa.Enum('RECEIPT', 'SHIPMENT', 'TRANSFER', name='movementtype'), nullable=False),
    sa.Column('reference_id', sa.UUID(), nullable=True),
    sa.Column('reference_type', sa.String(), nullable=True),
    sa.Column('movement_date', sa.DateTime(), nullable=False),
    sa.Column('recorded_by', sa.String(), nullable=False),
    sa.Column('batch_number', sa.String(), nullable=True),
    sa.Column('expiry_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['from_location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.ForeignKeyConstraint(['to_location_id'], ['locations.location_id'], ),
    sa.PrimaryKeyConstraint('movement_id')
    )
    op.create_table('invoice_items',
    sa.Column('invoice_item_id', sa.UUID(), nullable=False),
    sa.Column('invoice_id', sa.UUID(), nullable=False),
    sa.Column('item_description', sa.String(length=255), nullable=False),
    sa.Column('related_to', sa.Enum('shipment', 'storage', 'handling', 'other', name='invoice_item_related_to'), nullable=False),
    sa.Column('related_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('tax_rate', sa.Float(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['invoice_id'], ['billing.invoice_id'], ),
    sa.PrimaryKeyConstraint('invoice_item_id')
    )
    op.create_table('shipments',
    sa.Column('shipment_id', sa.UUID(), nullable=False),
    sa.Column('shipment_reference', sa.String(length=50), nullable=False),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.Column('carrier_id', sa.UUID(), nullable=True),
    sa.Column('vehicle_id', sa.UUID(), nullable=True),
    sa.Column('driver_id', sa.UUID(), nullable=True),
    sa.Column('origin_location_id', sa.UUID(), nullable=False),
    sa.Column('destination_location_id', sa.UUID(), nullable=False),
    sa.Column('planned_departure', sa.DateTime(), nullable=True),
    sa.Column('actual_departure', sa.DateTime(), nullable=True),
    sa.Column('planned_arrival', sa.DateTime(), nullable=True),
    sa.Column('actual_arrival', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('PLANNED', 'IN_TRANSIT', 'DELIVERED', 'CANCELED', name='shipmentstatusenum'), nullable=False),
    sa.Column('shipping_method', sa.Enum('ROAD', 'AIR', 'SEA', 'RAIL', name='shippingmethodenum'), nullable=True),
    sa.Column('tracking_number', sa.String(length=100), nullable=True),
    sa.Column('total_weight', sa.Float(), nullable=True),
    sa.Column('total_volume', sa.Float(), nullable=True),
    sa.Column('bill_of_lading_number', sa.String(length=100), nullable=True),
    sa.Column('shipping_cost', sa.Float(), nullable=True),
    sa.Column('fuel_surcharge', sa.Float(), nullable=True),
    sa.Column('accessorial_charges', sa.Float(), nullable=True),
    sa.Column('temperature_monitoring', sa.Boolean(), nullable=True),
    sa.Column('seal_number', sa.String(length=100), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['carrier_id'], ['carriers.carrier_id'], ),
    sa.ForeignKeyConstraint(['destination_location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.driver_id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['origin_location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.vehicle_id'], ),
    sa.PrimaryKeyConstraint('shipment_id'),
    sa.UniqueConstraint('shipment_reference'),
    sa.UniqueConstraint('tracking_number')
    )
    op.create_table('order_items',
    sa.Column('order_item_id', sa.UUID(), nullable=False),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('unit_weight', sa.Float(), nullable=False),
    sa.Column('unit_volume', sa.Float(), nullable=False),
    sa.Column('handling_instructions', sa.String(length=255), nullable=True),
    sa.Column('inventory_source_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['inventory_source_id'], ['inventory.inventory_id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('order_item_id')
    )
    op.create_table('shipment_orders',
    sa.Column('shipment_order_id', sa.UUID(), nullable=False),
    sa.Column('shipment_id', sa.UUID(), nullable=False),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('loading_sequence', sa.Integer(), nullable=False),
    sa.Column('unloading_sequence', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['shipment_id'], ['shipments.shipment_id'], ),
    sa.PrimaryKeyConstraint('shipment_order_id')
    )
    op.create_table('tracking_events',
    sa.Column('tracking_event_id', sa.UUID(), nullable=False),
    sa.Column('shipment_id', sa.UUID(), nullable=False),
    sa.Column('event_type', sa.String(), nullable=False),
    sa.Column('event_time', sa.DateTime(), nullable=False),
    sa.Column('location_id', sa.UUID(), nullable=False),
    sa.Column('gps_coordinates', sa.String(), nullable=True),
    sa.Column('event_description', sa.String(), nullable=True),
    sa.Column('recorded_by', sa.String(), nullable=False),
    sa.Column('signature', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['shipment_id'], ['shipments.shipment_id'], ),
    sa.PrimaryKeyConstraint('tracking_event_id')
    )
    op.create_table('customer_feedback',
    sa.Column('feedback_id', sa.UUID(), nullable=False),
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('order_item_id', sa.UUID(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('feedback_date', sa.Date(), nullable=False),
    sa.Column('follow_up_required', sa.Boolean(), nullable=True),
    sa.Column('follow_up_status', sa.String(length=50), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=False),
    sa.Column('updated_at', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], ),
    sa.ForeignKeyConstraint(['order_item_id'], ['order_items.order_item_id'], ),
    sa.PrimaryKeyConstraint('feedback_id')
    )
    op.create_table('driver_ratings',
    sa.Column('rating_id', sa.UUID(), nullable=False),
    sa.Column('driver_id', sa.UUID(), nullable=False),
    sa.Column('order_item_id', sa.UUID(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('rating_date', sa.Date(), nullable=False),
    sa.Column('follow_up_required', sa.Boolean(), nullable=True),
    sa.Column('follow_up_status', sa.Enum('open', 'resolved', 'pending', name='follow_up_status_enum'), nullable=True),
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=False),
    sa.Column('updated_at', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.driver_id'], ),
    sa.ForeignKeyConstraint(['order_item_id'], ['order_items.order_item_id'], ),
    sa.PrimaryKeyConstraint('rating_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('driver_ratings')
    op.drop_table('customer_feedback')
    op.drop_table('tracking_events')
    op.drop_table('shipment_orders')
    op.drop_table('order_items')
    op.drop_table('shipments')
    op.drop_table('invoice_items')
    op.drop_table('inventory_movements')
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_index('idx_inventory_product_id')
        batch_op.drop_index('idx_inventory_location_id')

    op.drop_table('inventory')
    op.drop_table('audit_logs')
    op.drop_table('warehouse_operations')
    op.drop_table('vehicles')
    op.drop_table('system_users')
    op.drop_table('rates')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('drivers')
    op.drop_table('billing')
    op.drop_table('third_party_services')
    op.drop_table('notifications')
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.drop_index('idx_location_type')
        batch_op.drop_index('idx_location_city_country')

    op.drop_table('locations')
    op.drop_table('incidents')
    op.drop_table('employees')
    op.drop_table('clients')
    op.drop_table('carriers')
    # ### end Alembic commands ###

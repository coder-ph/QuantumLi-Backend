from uuid import uuid4
from sqlalchemy import Column, String, Boolean, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from   app import db

class ThirdPartyService(db.Model):
    __tablename__ = "third_party_services"

    service_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    service_name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)

    contact_info = Column(String(150), nullable=True)

    authentication_method = Column(Enum('api_key', 'oauth2', 'basic_auth', 'jwt', name='authentication_method_enum'), nullable=False)

    config_details = Column(JSONB, nullable=False)

    active_status = Column(Boolean, default=True)

    integration_logs = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional relationship with integration logs, assuming there’s an IntegrationLog model
    # integration_log = db.relationship('IntegrationLog', backref='third_party_service', lazy=True)

    def __repr__(self):
        return f"<ThirdPartyService(service_name={self.service_name}, type={self.type}, active_status={self.active_status})>"

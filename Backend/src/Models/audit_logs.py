from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from   src.startup.database import db
from datetime import datetime

class Audit_Logs(db.Model):
    __tablename__ = 'audit_logs'

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('system_users.user_id'), nullable=False)
    action_type = Column(String(50), nullable=False)
    affected_table = Column(String(100), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    user = db.relationship('System_Users', back_populates='audit_logs')

    def __repr__(self):
        return f"<Audit_Logs(log_id={self.log_id}, user_id={self.user_id}, action_type={self.action_type}, affected_table={self.affected_table})>"

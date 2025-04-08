from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from   src.startup.database import db
from datetime import datetime
from src.utils.logger import logger

class System_Users(db.Model):
    __tablename__ = 'system_users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # employee_id = Column(UUID(as_uuid=True), ForeignKey('employees.employee_id'), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(Integer, nullable=False)
    role = Column(Enum('admin', 'employee', 'driver','user', 'manager', name='user_role_enum'), nullable=False)
    last_login = Column(DateTime, nullable=True, default=None)
    is_active = Column(Boolean, default=True)
    password_reset_token = Column(String(255), nullable=True)
    password_expiry = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # employee = db.relationship('Employee', back_populates='system_user', uselist=False, lazy='select')
    audit_logs = db.relationship('Audit_Logs', back_populates='user')
    def __repr__(self):
        return f"<System_Users(user_id={self.user_id}, username={self.username}, role={self.role}, is_active={self.is_active}, is_deleted={self.is_deleted})>"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"User {self.username} saved successfully.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving user {self.username}: {str(e)}")
            raise

    def update(self):
        try:
            db.session.commit()
            logger.info(f"User {self.username} updated successfully.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating user {self.username}: {str(e)}")
            raise

    def delete(self):
        try:
            self.is_deleted = True
            db.session.commit()
            logger.info(f"User {self.username} marked as deleted.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting user {self.username}: {str(e)}")
            raise

    def restore(self):
        try:
            self.is_deleted = False
            db.session.commit()
            logger.info(f"User {self.username} restored successfully.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error restoring user {self.username}: {str(e)}")
            raise

    def is_password_expired(self):
        if self.password_expiry and self.password_expiry < datetime.utcnow():
            logger.warning(f"Password for user {self.username} has expired.")
            return True
        return False

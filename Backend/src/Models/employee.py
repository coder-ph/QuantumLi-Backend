import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from Backend.src.startup.database import db
from src.utils.logger import logger  

class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    hire_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    termination_date = Column(DateTime, nullable=True)
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey('employees.employee_id'), nullable=True)
    access_level = Column(String(50), nullable=False)  
    login_credentials = Column(String(255), nullable=False)  
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)  

    supervisor = relationship('Employee', remote_side=[employee_id], backref='subordinates', lazy=True)

    def __repr__(self):
        return f"<Employee(id={self.employee_id}, name={self.first_name} {self.last_name}, position={self.position})>"

    def delete(self):
        """Soft delete functionality"""
        self.is_deleted = True
        db.session.commit()
        logger.info(f"Employee {self.employee_id} soft deleted.")

    def restore(self):
        """Restore soft-deleted entry"""
        self.is_deleted = False
        db.session.commit()
        logger.info(f"Employee {self.employee_id} restored.")

    def save(self):
        """Save a new employee"""
        db.session.add(self)
        db.session.commit()
        logger.info(f"Employee {self.employee_id} created.")

    def update(self):
        """Update an existing employee"""
        db.session.commit()
        logger.info(f"Employee {self.employee_id} updated.")

import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from  src.startup.database import db
from src.Models.base_model import BaseModel
from src.utils.logger import logger
import enum

class OperationStatus(enum.Enum):
    IN_PROGRESS = 'in progress'
    COMPLETED = 'completed'
    PENDING = 'pending'
    CANCELED = 'canceled'

class WarehouseOperation(BaseModel):
    __tablename__ = 'warehouse_operations'

    operation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.location_id'), nullable=False)
    operation_type = Column(String, nullable=False) 
    reference_id = Column(UUID(as_uuid=True), nullable=False)  
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    operator_id = Column(UUID(as_uuid=True), ForeignKey('employees.employee_id'), nullable=False)
    status = Column(Enum(OperationStatus), nullable=False, default=OperationStatus.PENDING)  
    equipment_used = Column(String, nullable=True)  
    notes = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    location = relationship('Location', backref='warehouse_operations', lazy=True)
    operator = relationship('Employee', backref='warehouse_operations', lazy=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<WarehouseOperation(id={self.operation_id}, operation_type={self.operation_type}, status={self.status})>"

    def log_creation(self):
      
        logger.info(f"WarehouseOperation with ID {self.operation_id} created at {self.created_at}.")

    def log_update(self):
       
        logger.info(f"WarehouseOperation with ID {self.operation_id} updated at {self.updated_at}.")

    def delete(self):
       
        self.deleted_at = datetime.utcnow()
        db.session.commit()
        logger.info(f"WarehouseOperation with ID {self.operation_id} marked as deleted at {self.deleted_at}.")
        
    @classmethod
    def query(cls):
        
        return db.session.query(cls).filter(cls.deleted_at == None)
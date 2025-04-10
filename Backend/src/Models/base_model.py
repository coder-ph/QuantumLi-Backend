from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from src.utils.logger import logger
from   src.startup.database import db

class BaseModel(db.Model):
    __abstract__ = True

    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def soft_delete(self):
        
        self.is_deleted = True
        logger.info(f"Soft delete applied to {self.__class__.__name__} with ID {getattr(self, 'id', 'unknown')}.")
        
    def log_creation(self):
        
        logger.info(f"{self.__class__.__name__} with ID {getattr(self, 'id', 'unknown')} created at {self.created_at}.")
        
    def log_update(self):
       
        logger.info(f"{self.__class__.__name__} with ID {getattr(self, 'id', 'unknown')} updated at {self.updated_at}.")
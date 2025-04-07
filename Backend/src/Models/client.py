import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from Backend.src.startup.database import db
from sqlalchemy import UniqueConstraint

class Client(db.Model):
    __tablename__ = 'clients'
    
    
    client_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
   
    company_name = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(14), nullable=False)  
    address = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)
    registration_number = Column(String(50), nullable=True)
    
    account_status = Column(Enum('active', 'inactive', name='account_status'), default='active')
    
    credit_limit = Column(Float, nullable=True)
    payment_terms = Column(String(50), nullable=True)
    
    date_created = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('email', name='uq_client_email'),
        UniqueConstraint('tax_id', name='uq_client_tax_id'),
        UniqueConstraint('registration_number', name='uq_client_registration_number'),
    )
    def __repr__(self):
        return f"<Client(client_id={self.client_id}, company_name={self.company_name}, email={self.email})>"

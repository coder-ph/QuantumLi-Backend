import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.Models.base_model import BaseModel

class Document(BaseModel):
    __tablename__ = 'documents'

    document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_name = Column(String(255), nullable=False)
    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), nullable=False)
    type = Column(String(100), nullable=False)
    file_url = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default='pending')  
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(Date, nullable=True)

   
    __table_args__ = (Index('ix_documents_driver_id', 'driver_id'),)

    driver = relationship('Driver', back_populates='documents')

    def __repr__(self):
        return f"<Document(document_id={self.document_id}, type={self.type}, status={self.status})>"
    
    def to_dict(self):
        return {
            'document_id': str(self.document_id),
            'document_name': self.document_name,
            'driver_id': str(self.driver_id),
            'type': self.type,
            'file_url': self.file_url,
            'status': self.status,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None
        }

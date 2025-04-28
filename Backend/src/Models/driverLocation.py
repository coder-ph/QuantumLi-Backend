# import uuid
# import logging
# from datetime import datetime
# from src.Models.base_model import BaseModel
# from sqlalchemy import Column, Date, ForeignKey, Float
# from sqlalchemy.dialects.postgresql import UUID
# from   src.startup.database import db

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class DriverLocation(db.Model):
#     __tablename__ = 'driver_locations'
    
#     driver_location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), unique=True, nullable=False)
#     latitude = Column(Float, nullable=False)
#     longitude = Column(Float, nullable=False)
#     updated_at = Column(Date, nullable=False, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<DriverLocation(driver_location_id={self.driver_location_id}, driver_id={self.driver_id}, latitude={self.latitude}, longitude={self.longitude}, updated_at={self.updated_at})>"

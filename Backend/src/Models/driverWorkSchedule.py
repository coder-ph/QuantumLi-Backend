import uuid
import logging
from datetime import datetime, time, date
from sqlalchemy import Column, String, Integer, Date, Time, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.Models.base_model import BaseModel
from src.startup.database import db

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DriverRecurringSchedule(BaseModel):
    __tablename__ = 'driver_recurring_schedules'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), nullable=False)
    day_of_week = Column(String(10), nullable=False)  
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)

    driver = relationship('Driver', backref='recurring_schedules', lazy=True)

class DriverOffDay(BaseModel):
    __tablename__ = 'driver_off_days'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), nullable=False)
    off_date = Column(Date, nullable=False)
    reason = Column(String(255), nullable=True) 

    driver = relationship('Driver', backref='off_days', lazy=True)


# class DriverWorkSchedule(BaseModel):
#     __tablename__ = 'driver_work_schedules'

#     schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'))
#     work_date = Column(Date, nullable=False)
#     start_time = Column(Time, nullable=False)
#     end_time = Column(Time, nullable=False)
#     is_available = Column(Boolean, nullable=False, default=True)

#     # Relationship
#     driver = relationship('Driver', back_ref='work_schedules', lazy=True)

#     def __repr__(self):
#         return (f'<DriverWorkSchedule(schedule_id={self.schedule_id}, driver_id={self.driver_id}, work_date={self.work_date}, start_time={self.start_time}, end_time={self.end_time}, is_available={self.is_available})>')
    

#     # ensure start time is before end time
#     @staticmethod
#     def validate_time_slot(start_time, end_time):
#         if start_time >= end_time:
#             logger.error(f"Invalid time slot: start_time {start_time} is not before end time {end_time}.")
#             raise ValueError("Start time must be before end time.")
#         logger.info(f"Valid time slot: {start_time} - {end_time}")
#         return start_time, end_time
    
#     # validate work date check that it's today or in the future
#     @staticmethod
#     def validate_work_date(work_date):
#         if work_date < datetime.utcnow().date():
#             logger.error(f"Invalid work date: {work_date}. Date cannot be in the past.")
#             raise ValueError("Work date cannot be in the past")
#         logger.info(f"Valid work date: {work_date}")
#         return work_date

import uuid
import logging
# from datetime import datetime, time, date
from sqlalchemy import Column, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.Models.base_model import BaseModel
from src.startup.database import db

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DriverSchedule(BaseModel):
    
    __tablename__ = 'driver_schedules'

    schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id = Column(UUID(as_uuid=True), ForeignKey('drivers.driver_id'), nullable=False, unique=True)

    weekly_schedule = Column(JSON, nullable=False, default=lambda: {
        day: {"work": False, "start": None, "end": None}
        for day in DAYS
    })

    # Relationship to the Driver model
    driver = relationship("Driver", backref="schedule", lazy=True)



    # Check if a driver is available on a given day and time.       

    def is_available(self, day_name, time_str):
        # Get the work schedule for the provided day
        day_schedule = self.weekly_schedule.get(day_name.lower())

        # If no schedule or the driver is off on that day
        if not day_schedule or not day_schedule.get("work"):
            return False

        # Get start and end times for the shift
        start = day_schedule.get("start")
        end = day_schedule.get("end")

        # If shift hours are missing, return False
        if not start or not end:
            return False

        # Return True if the given time is within shift hours
        return start <= time_str <= end



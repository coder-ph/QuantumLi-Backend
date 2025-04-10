from src.Models.drivers import Driver
from src.startup.database import db
from uuid import uuid4
from src.utils.logger import logger
from sqlalchemy.exc import SQLAlchemyError

class DriverRepository:

    def create(self, data):

        try:
            
            driver = Driver(**data)
            driver.validate_driver()  
           
            db.session.add(driver)
            db.session.commit()

            logger.info(f"Driver created successfully: {driver.driver_id}")
            return driver
        except SQLAlchemyError as e:
            db.session.rollback() 
            logger.error(f"Error creating driver: {str(e)}")
            raise Exception("Error creating driver.") from e

    def get_all(self):
        
        try:
            drivers = Driver.query.filter_by(is_deleted=False).all()
            logger.info(f"Retrieved {len(drivers)} active drivers.")
            return drivers
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving drivers: {str(e)}")
            raise Exception("Error retrieving drivers.") from e

    def get_by_id(self, driver_id):
        
        try:
            driver = Driver.query.filter_by(driver_id=driver_id, is_deleted=False).first()
            if driver:
                logger.info(f"Driver found: {driver.driver_id}")
            else:
                logger.warning(f"Driver with ID {driver_id} not found.")
            return driver
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving driver by ID {driver_id}: {str(e)}")
            raise Exception(f"Error retrieving driver with ID {driver_id}.") from e

    def update(self, driver, data):
      
        try:
            
            if not driver:
                logger.warning(f"Driver with ID {driver.driver_id} does not exist.")
                raise Exception("Driver not found.")

            for key, value in data.items():
                setattr(driver, key, value)

            driver.validate_driver()  

            db.session.commit()
            logger.info(f"Driver {driver.driver_id} updated successfully.")
            return driver
        except SQLAlchemyError as e:
            db.session.rollback()  
            logger.error(f"Error updating driver {driver.driver_id}: {str(e)}")
            raise Exception(f"Error updating driver {driver.driver_id}.") from e

    def delete(self, driver):
      
        try:
            if not driver:
                logger.warning("Attempted to delete a non-existing driver.")
                raise Exception("Driver not found.")

            driver.is_deleted = True
            db.session.commit()
            logger.info(f"Driver {driver.driver_id} marked as deleted.")
            return driver
        except SQLAlchemyError as e:
            db.session.rollback()  
            logger.error(f"Error deleting driver {driver.driver_id}: {str(e)}")
            raise Exception(f"Error deleting driver {driver.driver_id}.") from e

    def restore(self, driver):
       
        try:
            if not driver:
                logger.warning("Attempted to restore a non-existing driver.")
                raise Exception("Driver not found.")

            driver.is_deleted = False
            db.session.commit()
            logger.info(f"Driver {driver.driver_id} restored successfully.")
            return driver
        except SQLAlchemyError as e:
            db.session.rollback()  
            logger.error(f"Error restoring driver {driver.driver_id}: {str(e)}")
            raise Exception(f"Error restoring driver {driver.driver_id}.") from e

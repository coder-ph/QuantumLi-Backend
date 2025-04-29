from src.Models.drivers import Driver
# from src.Models.driverLocation import DriverLocation
from src.Models.documents import Document
from src.startup.database import db
from uuid import uuid4
from src.utils.logger import logger
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime
from Backend.src.Models.driverSchedule import DriverSchedule
from src.Models.drivers import Driver
from werkzeug.utils import secure_filename
import os
from datetime import datetime
class DriverRepository:

    def create_driver(self, data):
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

    def get_all_drivers(self):
        try:
            drivers = Driver.query.filter_by(is_deleted=False).all()
            logger.info(f"Retrieved {len(drivers)} active drivers.")
            return drivers
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving drivers: {str(e)}")
            raise Exception("Error retrieving drivers.") from e

    def get_driver_by_id(self, driver_id):
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

    def update_driver(self, driver, data):
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

    def delete_driver(self, driver):
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

    def restore_driver(self, driver):
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

    def create_document(self, data):
        try:
            if 'file' not in data:
                raise Exception("No file part in the request.")
            if data['file'].filename == '':
                raise Exception("No file selected.")

            filename = secure_filename(data['file'].filename)
            file_path = os.path.join('uploads', filename)

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            data['file'].save(file_path)

            document_type = data.get('type', 'unknown')

            expiry_date_str = data.get('expiry_date', None)
            if expiry_date_str:
                try:
                    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                except ValueError:
                    raise Exception("Invalid expiry date format. Use YYYY-MM-DD.")
            else:
                expiry_date = None

            document = Document(
                driver_id=data['driver_id'],
                document_name=data['document_name'],
                file_url=file_path,  
                status="pending",
                type=document_type,
                expiry_date=expiry_date  
            )

            db.session.add(document)
            db.session.commit()

            logger.info(f"Document created successfully: {document.document_id}")
            return document
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error creating document: {str(e)}")
            raise Exception("Error creating document.") from e
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            raise Exception(f"Error uploading document: {str(e)}")

    def get_documents_by_driver(self, driver_id):
        try:
            documents = Document.query.filter_by(driver_id=driver_id).all()
            logger.info(f"Retrieved {len(documents)} documents for driver {driver_id}.")
            return documents
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving documents for driver {driver_id}: {str(e)}")
            raise Exception(f"Error retrieving documents for driver {driver_id}.") from e

    def update_document_status(self, document_id, status):
        try:
            document = self.get_document_by_id(document_id)
            if not document:
                logger.warning(f"Document with ID {document_id} not found.")
                raise Exception("Document not found.")
            document.status = status
            db.session.commit()
            logger.info(f"Document {document_id} status updated to {status}.")
            return document
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating document {document_id} status: {str(e)}")
            raise Exception(f"Error updating document {document_id} status.") from e

    def get_document_by_id(self, document_id):
        try:
            document = Document.query.filter_by(document_id=document_id).first()
            if not document:
                logger.warning(f"Document with ID {document_id} not found.")
                return None
            return document
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving document by ID {document_id}: {str(e)}")
            raise Exception(f"Error retrieving document with ID {document_id}.") from e
        
    def update_all_driver_statuses(self):
        try:
            now = datetime.utcnow()
            current_day = now.strftime("%A").lower()
            current_time_str = now.strftime("%H:%M:%S")

            drivers = self.get_all_drivers()
            schedules = {schedule.driver_id: schedule for schedule in DriverSchedule.query.all()}

            changes_made = False

            for driver in drivers:
                schedule = schedules.get(driver.driver_id)
                if schedule and schedule.is_available(current_day, current_time_str):
                    if driver.status != "active":
                        driver.status = "active"
                        changes_made = True
                else:
                    if driver.status != "inactive":
                        driver.status = "inactive"
                        changes_made = True

            if changes_made:
                db.session.commit()
                logger.info("Drivers statuses updated successfully.")

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error changing status for driver: {str(e)}")
            raise Exception("Error changing status for driver.") from e

    
    
    def get_dispatch_queue(self):
        """
        Fetch drivers sorted by rating (descending) and load (ascending).
        Only include drivers who are eligible for dispatch (e.g., active status).
        """
        return Driver.query.filter_by(is_active=True).order_by(
            Driver.rating.desc(), 
            Driver.load.asc()     
        ).all()


    # def create_driver_location(self, data):

    #     try:
    #         driver_location = DriverLocation(**data)
    #         db.session.add(driver_location)
    #         db.session.commit()

    #         logger.info(f"Driver location created successfully: {driver_location.driver_location_id}")
    #         return driver_location
        
    #     except SQLAlchemyError as e:
    #         db.session.rollback() 
    #         logger.error(f"Error creating driver location: {str(e)}")
    #         raise Exception("Error creating driver location.") from e

    # def get_all_driver_location(self):

    #     try:
    #         driver_locations = DriverLocation.query.all()
    #         logger.info(f"Retrieved {len(driver_locations)} active driver locations.")
    #         return driver_locations
        
    #     except SQLAlchemyError as e:
    #         logger.error(f"Error retrieving driver locations: {str(e)}")
    #         raise Exception("Error retrieving drivers locations.") from e

    # def get_driver_location_by_id(self, driver_id):
        
    #     try:
    #         driver_location = DriverLocation.query.filter_by(driver_id=driver_id).first()
    #         if driver_location:
    #             logger.info(f"Driver location for driver ID {driver_id} found.")
    #         else:
    #             logger.warning(f"Driver location for driver ID {driver_id} not found.")
    #         return driver_location
        
    #     except SQLAlchemyError as e:
    #         logger.error(f"Error retrieving driver location by driver ID {driver_id}: {str(e)}")
    #         raise Exception(f"Error retrieving driver location of driver ID {driver_id}.") from e


    # def update_driver_location(self, driver_id, data):

    #     try:
    #         driver_location = DriverLocation.query.filter_by(driver_id=driver_id).first()
    #         if not driver_location:
    #             logger.error(f"Error retrieving driver location using driver ID {driver_id}")

    #         for key, value in data.items():
    #             setattr(driver_location, key, value)
            
    #         driver_location.updated_at = datetime.utcnow() 

    #         db.session.commit()
    #         logger.info(f"Driver location updated successfully")
            
    #         return driver_location
        
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         logger.error(f"Error updating driver {driver_id} location: {str(e)}")
    #         raise Exception(f"Error updating driver {driver_id}.") from e
        


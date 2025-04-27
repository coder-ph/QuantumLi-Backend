from src.Models.drivers import Driver
from src.Models.documents import Document
from src.startup.database import db
from uuid import uuid4
from src.utils.logger import logger
from sqlalchemy.exc import SQLAlchemyError
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

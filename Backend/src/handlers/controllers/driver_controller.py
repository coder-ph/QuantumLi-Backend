from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.driver_repository import DriverRepository
from src.decorators.permissions import role_required
from src.utils.logger import logger
from werkzeug.utils import secure_filename
import os
from src.startup.database import db


driver_repo = DriverRepository()

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager'])
def create_driver_view():
    data = request.get_json()
    try:
        driver = driver_repo.create_driver(data)
        logger.info(f"Driver created: ID {driver.driver_id}")
        return jsonify({"message": "Driver created successfully", "driver_id": str(driver.driver_id)}), 201
    except ValueError as e:
        logger.warning(f"Driver creation failed: {str(e)}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error creating driver: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager', 'employee'])
def get_all_drivers_view():
    try:
        drivers = driver_repo.get_all_drivers()
        return jsonify(drivers if drivers else []), 200
    except Exception as e:
        logger.error(f"Error fetching drivers: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager', 'employee'])
def get_driver_view(driver_id):
    try:
        driver = driver_repo.get_driver_by_id(driver_id)
        if not driver:
            return jsonify({"message": "Driver not found"}), 404
        return jsonify(driver), 200
    except Exception as e:
        logger.error(f"Error fetching driver {driver_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager'])
def update_driver_view(driver_id):
    data = request.get_json()
    try:
        driver = driver_repo.get_driver_by_id(driver_id)
        if not driver:
            return jsonify({"message": "Driver not found"}), 404
        updated_driver = driver_repo.update_driver(driver, data)
        logger.info(f"Driver {driver_id} updated.")
        return jsonify(updated_driver), 200
    except Exception as e:
        logger.error(f"Error updating driver {driver_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager'])
def delete_driver_view(driver_id):
    try:
        driver = driver_repo.get_driver_by_id(driver_id)
        if not driver:
            return jsonify({"message": "Driver not found"}), 404
        driver_repo.delete_driver(driver)
        logger.info(f"Driver {driver_id} deleted.")
        return jsonify({"message": "Driver deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting driver {driver_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager'])
def restore_driver_view(driver_id):
    try:
        driver = driver_repo.get_driver_by_id(driver_id)
        if not driver:
            return jsonify({"message": "Driver not found"}), 404
        driver_repo.restore_driver(driver)
        logger.info(f"Driver {driver_id} restored.")
        return jsonify({"message": "Driver restored successfully"}), 200
    except Exception as e:
        logger.error(f"Error restoring driver {driver_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

# New endpoints for document upload and verification

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager', 'employee'])
def upload_document_view(driver_id):
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        document_name = request.form.get('document_name')
        if not document_name:
            return jsonify({"error": "Document name is required"}), 400

        filename = secure_filename(file.filename)

        file_path = os.path.join('uploads', filename)

        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        file.save(file_path)

        document_data = {
            'driver_id': driver_id,
            'document_name': document_name,
            'file': file,
            'expiry_date': request.form.get('expiry_date', None)
        }

        document = driver_repo.create_document(document_data)

        return jsonify({"message": "Document uploaded successfully", "document_id": str(document.document_id)}), 201

    except Exception as e:
        logger.error(f"Error uploading document for driver {driver_id}: {str(e)}")
        return jsonify({"error": "Error uploading document", "details": str(e)}), 500

# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager'])
def update_document_status_view(document_id):
    try:
        status = request.json.get('status')
        if not status:
            return jsonify({"error": "Status is required"}), 400

        document = driver_repo.get_document_by_id(document_id)
        if not document:
            return jsonify({"error": "Document not found"}), 404

        document.status = status
        db.session.commit()

        logger.info(f"Document {document_id} status updated to {status}")
        return jsonify({"message": f"Document status updated to {status}", "document_id": str(document.document_id)}), 200

    except Exception as e:
        logger.error(f"Error updating document status for {document_id}: {str(e)}")
        return jsonify({"error": "Error updating document status", "details": str(e)}), 500


# @jwt_required()  # Authorization required
# @role_required(['admin', 'manager', 'employee'])
def get_documents_view(driver_id):
    try:
        documents = driver_repo.get_documents_by_driver(driver_id)
        documents_data = [document.to_dict() for document in documents]  # Convert each document to a dictionary
        return jsonify(documents_data if documents_data else []), 200
    except Exception as e:
        logger.error(f"Error fetching documents for driver {driver_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500


from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.driver_repository import DriverRepository
from src.decorators.permissions import role_required
from src.utils.logger import logger


driver_repo = DriverRepository()

@jwt_required()
@role_required(['admin', 'manager'])
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

@jwt_required()
@role_required(['admin', 'manager', 'employee'])
def get_all_drivers_view():
    try:
        drivers = driver_repo.get_all_drivers()
        return jsonify(drivers if drivers else []), 200
    except Exception as e:
        logger.error(f"Error fetching drivers: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager', 'employee'])
def get_driver_view(driver_id):
    try:
        driver = driver_repo.get_driver_by_id(driver_id)
        if not driver:
            return jsonify({"message": "Driver not found"}), 404
        return jsonify(driver), 200
    except Exception as e:
        logger.error(f"Error fetching driver {driver_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@role_required(['admin', 'manager'])
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

@jwt_required()
@role_required(['admin', 'manager'])
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

@jwt_required()
@role_required(['admin', 'manager'])
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
    

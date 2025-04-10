from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.handlers.repositories.driver_repository import DriverRepository
from src.services.auth_service import get_current_user
from src.error.apiErrors import UnauthorizedError, NotFoundError, BadRequestError
from src.utils.logger import logger

driver_repo = DriverRepository()

def is_authorized(user, allowed_roles):
    if user.role not in allowed_roles:
        raise UnauthorizedError(f"Role '{user.role}' not permitted for this action.")

@jwt_required()
def create_driver():
    user = get_current_user()
    is_authorized(user, ['admin'])

    data = request.get_json()
    
    
    if not data:
        raise BadRequestError("No data provided for driver creation.")
    
    
    try:
        driver = driver_repo.create(data)
        logger.info(f"User {user.email} created a new driver: {driver.driver_id}")
        return jsonify({'message': 'Driver created successfully.', 'driver_id': str(driver.driver_id)}), 201
    except Exception as e:
        logger.error(f"Error creating driver: {str(e)}")
        raise BadRequestError(f"Failed to create driver: {str(e)}")

@jwt_required()
def get_all_drivers():
    user = get_current_user()
    is_authorized(user, ['admin', 'manager'])

    try:
        drivers = driver_repo.get_all()
        if not drivers:
            return jsonify({'message': 'No drivers found.'}), 404
        logger.info(f"User {user.email} fetched all drivers.")
        return jsonify([driver.to_dict() for driver in drivers]), 200
    except Exception as e:
        logger.error(f"Error retrieving drivers: {str(e)}")
        return jsonify({'message': 'Failed to retrieve drivers.'}), 500

@jwt_required()
def get_driver(driver_id):
    user = get_current_user()
    is_authorized(user, ['admin', 'manager'])

    try:
        driver = driver_repo.get_by_id(driver_id)
        if not driver:
            raise NotFoundError("Driver not found.")
        logger.info(f"User {user.email} fetched driver: {driver.driver_id}")
        return jsonify(driver.to_dict()), 200
    except NotFoundError as e:
        logger.warning(f"Driver not found with ID {driver_id}.")
        raise e
    except Exception as e:
        logger.error(f"Error retrieving driver with ID {driver_id}: {str(e)}")
        return jsonify({'message': 'Failed to retrieve driver.'}), 500

@jwt_required()
def update_driver(driver_id):
    user = get_current_user()
    is_authorized(user, ['admin'])

    data = request.get_json()
    
    if not data:
        raise BadRequestError("No data provided for driver update.")

    try:
        driver = driver_repo.get_by_id(driver_id)
        if not driver:
            raise NotFoundError("Driver not found.")
        
       
        driver_repo.update(driver, data)
        logger.info(f"User {user.email} updated driver: {driver.driver_id}")
        return jsonify({'message': 'Driver updated successfully.'}), 200
    except NotFoundError as e:
        logger.warning(f"Driver with ID {driver_id} not found for update.")
        raise e
    except Exception as e:
        logger.error(f"Error updating driver {driver_id}: {str(e)}")
        return jsonify({'message': 'Failed to update driver.'}), 500

@jwt_required()
def delete_driver(driver_id):
    user = get_current_user()
    is_authorized(user, ['admin'])

    try:
        driver = driver_repo.get_by_id(driver_id)
        if not driver:
            raise NotFoundError("Driver not found.")
        
        driver_repo.delete(driver)
        logger.info(f"User {user.email} deleted driver: {driver.driver_id}")
        return jsonify({'message': 'Driver deleted successfully.'}), 200
    except NotFoundError as e:
        logger.warning(f"Driver with ID {driver_id} not found for deletion.")
        raise e
    except Exception as e:
        logger.error(f"Error deleting driver {driver_id}: {str(e)}")
        return jsonify({'message': 'Failed to delete driver.'}), 500

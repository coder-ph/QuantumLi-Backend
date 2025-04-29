from flask import jsonify
from flask_jwt_extended import jwt_required
from src.handlers.services.driver_assignment_service import DriverAssignmentService
from src.utils.logger import logger
from src.decorators.permissions import role_required


@jwt_required()
@role_required(['admin', 'manager'])
def assign_driver_view(order_id):
    """
    Endpoint to assign a driver to an order.

    Args:
        order_id (str): The ID of the order to assign a driver to.

    Returns:
        Response: JSON response with the result of the driver assignment.
    """
    try:
       
        driver_assignment_service = DriverAssignmentService()

  
        result, status_code = driver_assignment_service.assign_driver_to_order(order_id)

       
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error assigning driver to order {order_id}: {str(e)}", exc_info=True)
        return jsonify({"message": "Internal server error"}), 500
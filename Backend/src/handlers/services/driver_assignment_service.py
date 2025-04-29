from src.handlers.repositories.driver_repository import DriverRepository
from src.handlers.repositories.order_repository import get_order_by_id, update_order
from src.handlers.services.notification_service import NotificationService
from src.utils.logger import logger
from flask_mail import Message
from src.startup.mail import mail
import time

class DriverAssignmentService:
    def __init__(self):
        self.driver_repo = DriverRepository()

    def assign_driver_to_order(self, order_id):
        """
        Assign a driver to an order based on the dispatch queue.

        Args:
            order_id (str): The ID of the order to assign a driver to.

        Returns:
            tuple: A dictionary with the result message and an HTTP status code.
        """
        order = get_order_by_id(order_id)
        if not order:
            logger.error(f"Order {order_id} not found.")
            return {"message": "Order not found"}, 404

        candidates = self.driver_repo.get_dispatch_queue()  # Fetch drivers sorted by rating, load, etc.
        for driver in candidates:
            if driver.status != "active":
                logger.info(f"Skipping inactive driver {driver.driver_id}.")
                continue

            # Send notification to driver
            notification_id = NotificationService.create_notification(
                recipient_id=driver.driver_id,
                message=f"You have been assigned to Order {order_id}. Please respond.",
                type="task_assignment",
                related_entity="order",
                related_id=order_id,
                buttons=["Accept", "Reject"]
            )

            # Wait for driver response (timeout: 30 seconds)
            response = self._wait_for_driver_response(notification_id, timeout=30)

            if response == "Accepted":
                # Mark order as assigned
                order.driver_id = driver.driver_id
                update_order(order_id, {"driver_id": driver.driver_id, "status": "assigned"})
                logger.info(f"Order {order_id} assigned to driver {driver.driver_id}.")
                NotificationService.create_notification(
                    recipient_id=order.client_id,
                    message=f"Your order {order_id} has been assigned to driver {driver.driver_id}.",
                    type="confirmation"
                )
                return {"message": "Order assigned successfully"}, 200

            elif response == "Rejected":
                reason = self._get_rejection_reason(driver.driver_id, order_id)
                update_order(order_id, {"reason": reason})
                logger.info(f"Driver {driver.driver_id} rejected order {order_id} with reason: {reason}.")
                continue

            elif response == "Timeout":
                update_order(order_id, {"reason": "No response"})
                logger.info(f"Driver {driver.driver_id} did not respond to order {order_id}.")
                continue

        # If no drivers accepted, mark order as unassigned and trigger fallback 
        update_order(order_id, {"status": "unassigned"})
        self._trigger_fallback(order_id)
        logger.warning(f"Order {order_id} could not be assigned to any driver.")
        return {"message": "Order could not be assigned"}, 500

    def _wait_for_driver_response(self, notification_id, timeout):
        """
        Wait for a driver's response to a notification.

        Args:
            notification_id (str): The ID of the notification.
            timeout (int): The timeout in seconds.

        Returns:
            str: The driver's response ("Accepted", "Rejected", or "Timeout").
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = NotificationService.get_response(notification_id)
            if response:
                return response
            time.sleep(1)
        return "Timeout"

    def _get_rejection_reason(self, driver_id, order_id):
        """
        Get the reason for a driver's rejection.

        Args:
            driver_id (str): The ID of the driver.
            order_id (str): The ID of the order.

        Returns:
            str: The rejection reason.
        """
        
        reasons = ["Too far", "Busy", "Vehicle issue", "Other"]
       
        return reasons[0]  

    def _trigger_fallback(self, order_id):
        """
        Trigger a fallback mechanism when no driver accepts the order.

        Args:
            order_id (str): The ID of the order.
        """
        
        msg = Message(
            subject="Order Assignment Failed",
            sender="noreply@example.com",
            recipients=["fallback@example.com"],
            body=f"Order {order_id} could not be assigned to any driver. Please take manual action."
        )
        mail.send(msg)
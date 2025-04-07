import logging
import traceback
from app import app

class APIError(Exception):
    """Base class for all custom API errors."""
    def __init__(self, message, status_code=400, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

       
        self.log_error()

    def log_error(self):
        """Logs the error details."""
        app.logger.error(f"Error occurred: {self.message}, "
                         f"Status Code: {self.status_code}, "
                         f"Error Code: {self.error_code if self.error_code else 'N/A'}, "
                         f"Traceback: {traceback.format_exc()}")

class NotFoundError(APIError):
    """Raised when a resource is not found."""
    def __init__(self, message="Resource not found", status_code=404, error_code=None):
        super().__init__(message, status_code, error_code)

class ValidationError(APIError):
    """Raised when validation fails."""
    def __init__(self, message="Validation error", status_code=400, error_code=None):
        super().__init__(message, status_code, error_code)

class UnauthorizedError(APIError):
    """Raised when a user is unauthorized to access a resource."""
    def __init__(self, message="Unauthorized access", status_code=401, error_code=None):
        super().__init__(message, status_code, error_code)

class InternalServerError(APIError):
    """Raised for internal server errors."""
    def __init__(self, message="Internal server error", status_code=500, error_code=None):
        super().__init__(message, status_code, error_code)

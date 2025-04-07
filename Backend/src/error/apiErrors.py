import traceback
from src.utils.logger import logger  


class APIError(Exception):
    """
    Base class for all custom API errors.
    Supports custom message, status code, error code, and optional payload (dict).
    """

    def __init__(self, message, status_code=400, error_code=None, payload=None, log=True):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "api_error"
        self.payload = payload or {}
        super().__init__(message)

        if log:
            self.log_error()

    def log_error(self):
        tb = traceback.format_exc()
        log_message = {
            "message": self.message,
            "status_code": self.status_code,
            "error_code": self.error_code,
            "payload": self.payload,
            "traceback": tb if "NoneType" not in tb else "No traceback available"
        }
        logger.error(f"APIError Logged: {log_message}")

    def to_dict(self):
        return {
            "error": {
                "message": self.message,
                "code": self.error_code,
                "status": self.status_code,
                "details": self.payload
            }
        }

    def __str__(self):
        return f"{self.status_code} {self.error_code}: {self.message}"


class NotFoundError(APIError):
    def __init__(self, message="Resource not found", error_code="not_found", payload=None):
        super().__init__(message, 404, error_code, payload)


class ValidationError(APIError):
    def __init__(self, message="Validation failed", error_code="validation_error", payload=None):
        super().__init__(message, 400, error_code, payload)


class UnauthorizedError(APIError):
    def __init__(self, message="Unauthorized", error_code="unauthorized", payload=None):
        super().__init__(message, 401, error_code, payload)


class ForbiddenError(APIError):
    def __init__(self, message="Forbidden", error_code="forbidden", payload=None):
        super().__init__(message, 403, error_code, payload)


class InternalServerError(APIError):
    def __init__(self, message="An unexpected error occurred", error_code="internal_server_error", payload=None):
        super().__init__(message, 500, error_code, payload)

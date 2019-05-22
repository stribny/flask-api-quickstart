from flask import jsonify


class AppError(Exception):
    """Base class for all errors. Can represent error as HTTP response for API calls"""

    status_code = 500
    error_code = "INTERNAL_ERROR"
    message = "Request cannot be processed at the moment."

    def __init__(self, status_code=None, error_code=None, message=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code

    def to_api_response(self):
        response = jsonify(
            {"errorCode": self.error_code, "errorMessage": self.message}
        )
        response.status_code = self.status_code
        return response


class InvalidFieldError(AppError):
    def __init__(self, field_name, message=""):
        AppError.__init__(
            self,
            status_code=422,
            error_code="INVALID_FIELD",
            message=f"Invalid '{field_name}''. {message}",
        )


class BadRequestError(AppError):
    def __init__(self, message="Malformed request."):
        AppError.__init__(
            self, status_code=400, error_code="BAD_REQUEST", message=message
        )


class NotFoundError(AppError):
    def __init__(self, message="Requested resource not found."):
        AppError.__init__(
            self, status_code=404, error_code="NOT_FOUND", message=message
        )


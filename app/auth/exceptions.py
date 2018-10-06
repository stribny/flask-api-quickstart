from app.exceptions import AppError


class InvalidCredentialsError(AppError):
    def __init__(self):
        AppError.__init__(
            self,
            status_code=401,
            error_code="INVALID_CREDENTIALS",
            message="Invalid username or password.",
        )


class InvalidTokenError(AppError):
    def __init__(self):
        AppError.__init__(
            self,
            status_code=401,
            error_code="INVALID_TOKEN",
            message="Token is invalid or missing.",
        )


class TokenExpiredError(AppError):
    def __init__(self):
        AppError.__init__(
            self,
            status_code=401,
            error_code="TOKEN_EXPIRED",
            message="Authentication token has expired.",
        )

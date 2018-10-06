from functools import wraps

from flask import request

from app.auth.exceptions import InvalidTokenError, TokenExpiredError
from app.auth.service import decode_auth_token, is_token_blacklisted
from app.models import User


def get_token_from_header():
    token = None
    if "Authorization" in request.headers:
        auth_header = request.headers["Authorization"]
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            token = None
    return token


def auth_required(f):
    """Decorator to require auth token on marked endpoint"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            raise InvalidTokenError()

        if is_token_blacklisted(token):
            raise TokenExpiredError()

        token_payload = decode_auth_token(token)

        current_user = User.query.filter_by(id=token_payload["sub"]).first()
        if not current_user:
            raise InvalidTokenError()

        return f(*args, **kwargs)

    return decorated_function

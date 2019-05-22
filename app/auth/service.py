import datetime
import bcrypt
import jwt
from usernames import is_safe_username
from validate_email import validate_email

from app import app, db
from app.auth.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    TokenExpiredError,
)
from app.exceptions import InvalidFieldError
from app.models import BlacklistToken, User
from app.utils import now

ENCODING = "utf-8"


def create_user(username, email, password):
    if not is_safe_username(username):
        raise InvalidFieldError(
            "username", "Username contains forbidden characters or is a reserved word."
        )

    if len(username) < 5:
        raise InvalidFieldError(
            "username", "Username has to be at least 5 characters long."
        )

    if len(password) < 8:
        raise InvalidFieldError(
            "password", "Password has to be at least 8 characters long."
        )

    if not validate_email(email):
        raise InvalidFieldError("email")

    email_used = True if User.query.filter_by(email=email).first() else False
    if email_used:
        raise InvalidFieldError("email", "Email address is already used.")

    username_used = True if User.query.filter_by(username=username).first() else False
    if username_used:
        raise InvalidFieldError("username", "Username is already used.")

    hashed_password = hash_password(password)
    user = User(username, email, hashed_password, now())
    db.session.add(user)
    db.session.commit()


def login_user(username, password):
    """Generate a new auth token for the user"""
    saved_user = User.query.filter_by(username=username).first()
    if saved_user and check_password(password, saved_user.password):
        token = encode_auth_token(saved_user.id)
        return token
    else:
        raise InvalidCredentialsError()


def hash_password(password):
    return bcrypt.hashpw(password.encode(ENCODING), bcrypt.gensalt()).decode(ENCODING)


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(ENCODING), hashed_password.encode(ENCODING))


def encode_auth_token(user_id):
    """Create a token with user_id and expiration date using secret key"""
    exp_days = app.config.get("AUTH_TOKEN_EXPIRATION_DAYS")
    exp_seconds = app.config.get("AUTH_TOKEN_EXPIRATION_SECONDS")
    exp_date = now() + datetime.timedelta(
        days=exp_days, seconds=exp_seconds
    )
    payload = {"exp": exp_date, "iat": now(), "sub": user_id}
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256").decode(
        ENCODING
    )


def decode_auth_token(token):
    """Convert token to original payload using secret key if the token is valid"""
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError as ex:
        raise TokenExpiredError() from ex
    except jwt.InvalidTokenError as ex:
        raise InvalidTokenError() from ex


def blacklist_token(token):
    bl_token = BlacklistToken(token, now())
    db.session.add(bl_token)
    db.session.commit()


def is_token_blacklisted(token):
    bl_token = BlacklistToken.query.filter_by(token=token).first()
    return True if bl_token else False

from flask import Blueprint, jsonify, request

from app.auth.helpers import auth_required, get_token_from_header
from app.auth.service import (
    blacklist_token,
    create_user,
    is_token_blacklisted,
    login_user,
)
from app.exceptions import BadRequestError

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/signup", methods=["POST"])
def signup():
    if not request.json:
        raise BadRequestError()
    if not "username" in request.json:
        raise BadRequestError("'username' field is missing.")
    if not "password" in request.json:
        raise BadRequestError("'password' field is missing.")
    if not "email" in request.json:
        raise BadRequestError("'email' field is missing.")

    create_user(
        request.json["username"], request.json["email"], request.json["password"]
    )

    return jsonify({"success": True})


@auth_api.route("/login", methods=["POST"])
def login():
    if not request.json:
        raise BadRequestError()
    if not "username" in request.json:
        raise BadRequestError("'username' field is missing.")
    if not "password" in request.json:
        raise BadRequestError("'password' field is missing.")

    token = login_user(request.json["username"], request.json["password"])
    return jsonify({"token": token})


@auth_api.route("/logout", methods=["POST"])
@auth_required
def logout():
    token = get_token_from_header()
    blacklist_token(token)
    return jsonify({"success": True})

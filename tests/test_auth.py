import json

from tests.helpers import (
    assert_error,
    assert_error_invalid_field,
    assert_error_missing_field,
    assert_error_token_expired,
    assert_success_200,
    get_valid_token,
    login_user,
    signup_user,
)


def test_signup_success(client):
    response = signup_user(
        client=client,
        username="username1",
        email="mail@example.com",
        password="Password1",
    )
    assert_success_200(response)
    data = json.loads(response.data)
    assert data["success"] == True


def test_signup_missing_username(client):
    response = signup_user(
        client=client, username=None, email="mail@example.com", password="Password1"
    )
    assert_error_missing_field(response, "username")


def test_signup_missing_email(client):
    response = signup_user(
        client=client, username="username1", email=None, password="Password1"
    )
    assert_error_missing_field(response, "email")


def test_signup_missing_password(client):
    response = signup_user(
        client=client, username="username1", email="mail@example.com", password=None
    )
    assert_error_missing_field(response, "password")


def test_signup_invalid_username_too_short(client):
    response = signup_user(
        client=client, username="adam", email="mail@example.com", password="Password1"
    )
    assert_error_invalid_field(response, "username")


def test_signup_invalid_username_forbidden_chars(client):
    response = signup_user(
        client=client,
        username=" -- -- -- ",
        email="mail@example.com",
        password="Password1",
    )
    assert_error_invalid_field(response, "username")


def test_signup_invalid_email(client):
    response = signup_user(
        client=client,
        username="username1",
        email="mailexample.com",
        password="Password1",
    )
    assert_error_invalid_field(response, "email")


def test_signup_invalid_password_too_short(client):
    response = signup_user(
        client=client, username="username1", email="mail@example.com", password="1234"
    )
    assert_error_invalid_field(response, "password")


def test_signup_username_already_used(client):
    username = "username1"
    password = "Password1"
    signup_user(
        client=client, username=username, email="email@mail.com", password=password
    )
    response = signup_user(
        client=client, username=username, email="email2@mail.com", password=password
    )
    assert_error(response, 422)
    data = json.loads(response.data)
    assert data["errorCode"] == "INVALID_FIELD"
    assert "Username is already used" in data["errorMessage"]


def test_signup_email_already_used(client):
    email = "email@mail.com"
    password = "Password1"
    signup_user(client=client, username="username1", email=email, password=password)
    response = signup_user(
        client=client, username="username2", email=email, password=password
    )
    assert_error(response, 422)
    data = json.loads(response.data)
    assert data["errorCode"] == "INVALID_FIELD"
    assert "Email address is already used" in data["errorMessage"]


def test_login_success(client):
    username = "username1"
    email = "user1@example.com"
    password = "Password1"
    signup_user(client=client, username=username, email=email, password=password)
    response = login_user(client=client, username=username, password=password)
    assert_success_200(response)
    data = json.loads(response.data)
    assert data["token"]


def test_login_bad_credentials(client):
    username = "username1"
    email = "user1@example.com"
    password = "Password1"
    signup_user(client=client, username=username, email=email, password=password)
    response = login_user(client=client, username=username, password="Password2")
    assert_error(response, 401)
    data = json.loads(response.data)
    assert data["errorCode"] == "INVALID_CREDENTIALS"
    assert not "token" in data


def test_logout(client):
    token = get_valid_token(client)
    response = client.post(
        "/api/v1/auth/logout",
        headers=dict(Authorization="Bearer " + token),
        content_type="application/json",
    )
    assert_success_200(response)
    response_protected = client.get(
        "/protected",
        headers=dict(Authorization="Bearer " + token),
        content_type="application/json",
    )
    assert_error_token_expired(response_protected)

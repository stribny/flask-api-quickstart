import json

from tests.helpers import (
    assert_error,
    assert_error_invalid_token,
    assert_success_200,
    get_valid_token,
    login_user,
    signup_user,
)


def test_ping(client):
    response = client.get("/ping")
    data = json.loads(response.data)
    assert_success_200(response)
    assert data["status"] == "running"


def test_access_protected_endpoint_with_valid_token(client):
    token = get_valid_token(client)
    response = client.get(
        "/protected",
        headers=dict(Authorization="Bearer " + token),
        content_type="application/json",
    )
    assert_success_200(response)
    data = json.loads(response.data)
    assert data["message"] == "Protected message"


def test_access_protected_endpoint_without_token(client):
    response = client.get("/protected", content_type="application/json")
    assert_error_invalid_token(response)


def test_access_protected_endpoint_without_valid_token(client):
    token = "djkafkldhsfhl"
    response = client.get(
        "/protected",
        headers=dict(Authorization="Bearer " + token),
        content_type="application/json",
    )
    assert_error_invalid_token(response)

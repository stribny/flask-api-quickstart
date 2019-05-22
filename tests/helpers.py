import json


def signup_user(client, username, email, password):
    data = dict()
    if username:
        data["username"] = username
    if email:
        data["email"] = email
    if password:
        data["password"] = password

    return client.post(
        "/api/v1/auth/signup", content_type="application/json", data=json.dumps(data)
    )


def login_user(client, username, password):
    data = dict()
    if username:
        data["username"] = username
    if password:
        data["password"] = password

    return client.post(
        "/api/v1/auth/login", content_type="application/json", data=json.dumps(data)
    )


def get_valid_token(client):
    username = "usrname1"
    email = "usrname1@example.com"
    password = "Password1"
    signup_user(client=client, username=username, email=email, password=password)
    response = login_user(client=client, username=username, password=password)
    data = json.loads(response.data)
    return data["token"]


def assert_success_200(response):
    assert response.status_code == 200
    assert response.content_type == "application/json"


def assert_error(response, error_code):
    assert response.status_code == error_code
    assert response.content_type == "application/json"


def assert_error_invalid_token(response):
    assert_error(response, 401)
    data = json.loads(response.data)
    assert data["errorCode"] == "INVALID_TOKEN"


def assert_error_token_expired(response):
    assert_error(response, 401)
    data = json.loads(response.data)
    assert data["errorCode"] == "TOKEN_EXPIRED"


def assert_error_missing_field(response, field):
    assert_error(response, 400)
    data = json.loads(response.data)
    assert data["errorCode"] == "BAD_REQUEST"
    assert field in data["errorMessage"]


def assert_error_invalid_field(response, field):
    assert_error(response, 422)
    data = json.loads(response.data)
    assert data["errorCode"] == "INVALID_FIELD"
    assert field in data["errorMessage"]

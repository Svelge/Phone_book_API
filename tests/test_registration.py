import uuid
from dataclasses import asdict

import pytest
import requests
from config import API_BASE_URL
from models.user import User


def test_registration_success(new_user):
    # unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"

    # payload = {
    #     "username": unique_email,
    #     "password": "Password123$"
    # }

    # user = User(
    #     username=unique_email,
    #     password="Password123$"
    # )
    payload = asdict(new_user)

    response = requests.post(f"{API_BASE_URL}v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "token" in body
    assert len(body["token"]) > 0



@pytest.mark.parametrize(
      "field,bad_value",
    [
      pytest.param("password","Pass12$", id="password_too_short"),
      pytest.param("password","password123$", id="password_no_uppercase"),
      pytest.param("password","PASSWORD123$", id="password_no_lowercase"),
      pytest.param("password","PASSWORD$", id="password_no_digits"),
      pytest.param("password","Password123", id="password_no_special_char"),
      pytest.param("password","PASSWORD123$fddgjhdkfjhfdkhj", id="password_too_long"),
      pytest.param("username","user@", id="username_no_domain"),
      pytest.param("username","notanemail", id="username_no_at_sign"),
      pytest.param("username","@gmail.com", id="username_no_local_part"),
    ]
)

def test_registration_with_invalid_value_rejected(new_user, field, bad_value):
    payload = asdict(new_user)
    payload[field] = bad_value

    response=requests.post(f"{API_BASE_URL}v1/user/registration/usernamepassword", json=payload)

    assert response.status_code == 400
    assert field in response.json()["message"]
    body = response.json()
    assert "token" not in body


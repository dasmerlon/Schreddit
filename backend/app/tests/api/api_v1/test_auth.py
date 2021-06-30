from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import User
from app.tests.utils.fake_payloads import UserPayloads


def test_get_access_token_by_email(client: TestClient, test_user_in_db: User) -> None:
    payload = UserPayloads.get_auth_by_email()
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert response.status_code == status.HTTP_200_OK

    access_token = response.json().get("access_token")
    assert access_token


def test_get_access_token_by_username(
    client: TestClient, test_user_in_db: User
) -> None:
    payload = UserPayloads.get_auth_by_username()
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert response.status_code == status.HTTP_200_OK

    access_token = response.json().get("access_token")
    assert access_token


@pytest.mark.parametrize(
    "payload",
    [
        {"username": settings.TEST_USER_EMAIL, "password": "wrong-password"},
        {"username": "adversary@example.com", "password": settings.TEST_USER_PASSWORD},
        {"username": "adversary@example.com", "password": "wrong-password"},
    ],
)
def test_get_access_token_by_email_wrong_input(
    client: TestClient, test_user_in_db: User, payload: Dict
) -> None:
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
    assert response.json().get("access_token") is None


@pytest.mark.parametrize(
    "payload",
    [
        {"username": settings.TEST_USER_USERNAME, "password": "wrong-password"},
        {"username": "adversary", "password": settings.TEST_USER_PASSWORD},
        {"username": "adversary", "password": "wrong-password"},
    ],
)
def test_get_access_token_by_username_wrong_input(
    client: TestClient, test_user_in_db: User, payload: Dict
) -> None:
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
    assert response.json().get("access_token") is None

from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.models import User
from app.tests.utils.fake_payloads import UserPayloads


def test_get_access_token_by_email(client: TestClient, test_user_in_db: User) -> None:
    payload = UserPayloads.get_auth_by_email()
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert response.status_code == status.HTTP_200_OK

    # Ensure that the access token has been returned and is properly saved in Redis.
    access_token = response.json().get("access_token")
    assert access_token
    assert crud.redis.get(access_token).decode("utf-8")

    # Make sure that we can actually use the JWT token to access routes with
    # restricted access via a valid Authentication header.
    response = client.put(
        f"{settings.API_V1_STR}/users",
        json={"password": "hunter3"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Make sure that we can use the JWT token when it's not cached in Redis.
    crud.redis.delete(access_token)
    response = client.put(
        f"{settings.API_V1_STR}/users",
        json={"password": "hunter4"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_access_token_by_username(
    client: TestClient, test_user_in_db: User
) -> None:
    payload = UserPayloads.get_auth_by_username()
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert response.status_code == status.HTTP_200_OK

    # Ensure that the access token has been returned and is properly saved in Redis.
    access_token = response.json().get("access_token")
    assert access_token
    assert crud.redis.get(access_token).decode("utf-8")


def test_disallow_login_with_invalid_jwt(client: TestClient) -> None:
    # Make sure that we can't use an incorrect JWT token.
    response = client.put(
        f"{settings.API_V1_STR}/users",
        json={"password": "hunter3"},
        headers={"Authorization": "Bearer wrongtoken"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


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

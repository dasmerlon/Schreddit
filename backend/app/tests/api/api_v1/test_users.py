from typing import Dict, List

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models import User
from app.tests.utils.fake_payloads import UserPayloads


def test_register_user(client: TestClient, remove_users: List) -> None:
    payload = UserPayloads.get_create()
    r = client.post(f"{settings.API_V1_STR}/users", json=payload)
    registered_user = r.json()
    remove_users.append(registered_user["uid"])
    assert r.status_code == status.HTTP_201_CREATED
    assert registered_user["uid"] is not None
    assert registered_user["email"] == payload["email"]
    assert registered_user["username"] == payload["username"]


def test_register_existing_email(client: TestClient, test_user_in_db: User) -> None:
    payload = UserPayloads.get_create()
    payload["username"] = "newuser-samemail"
    r = client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in r.json()


def test_register_existing_username(client: TestClient, test_user_in_db: User) -> None:
    payload = UserPayloads.get_create()
    payload["email"] = "newmail@sameuser.com"
    r = client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in r.json()


def test_get_user(client: TestClient, test_user_in_db: User) -> None:
    payload = client.get(
        f"{settings.API_V1_STR}/users/u/{test_user_in_db.username}"
    ).json()
    assert payload["email"] == test_user_in_db.email
    assert payload["username"] == test_user_in_db.username


def test_get_not_existing_user(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/users/u/not_existing")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "new_email@example.com", "password": "hunter2"},
        {"email": "new_email@example.com"},
        {"password": "hunter2"},
    ],
)
def test_update_user(client: TestClient, fake_auth: User, payload: Dict) -> None:
    response = client.put(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated_user = crud.user.get_by_username(settings.TEST_USER_USERNAME)
    assert updated_user is not None

    for key, value in payload.items():
        if key == "password":
            assert verify_password(value, updated_user.hashed_password)
        else:
            assert getattr(updated_user, key) == value


@pytest.mark.parametrize(
    "payload",
    [
        {"email": settings.TEST_USER_EMAIL, "password": settings.TEST_USER_PASSWORD},
        {"email": settings.TEST_USER_EMAIL},
        {"password": settings.TEST_USER_PASSWORD},
        {},
    ],
)
def test_update_user_not_modified(
    client: TestClient, fake_auth: User, payload: Dict
) -> None:
    response = client.put(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_304_NOT_MODIFIED

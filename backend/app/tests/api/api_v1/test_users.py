import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models import User


def register_user(client, email, username, password):
    payload = {"email": email, "username": username, "password": password}
    return client.post(f"{settings.API_V1_STR}/users/register", json=payload)


def test_register_user(client: TestClient, database) -> None:
    email = "test@example.com"
    username = "test"
    password = "password"
    r = register_user(client, email, username, password)
    assert r.status_code == status.HTTP_201_CREATED
    registered_user = r.json()

    assert registered_user["email"] == email
    assert registered_user["username"] == username


def test_register_existing_email(client: TestClient, database) -> None:
    email = "dup@example.com"
    username1 = "dup1"
    username2 = "dup2"
    password = "password"
    register_user(client, email, username1, password)
    r = register_user(client, email, username2, password)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in r.json()


def test_register_existing_username(client: TestClient, database) -> None:
    email1 = "dup1@example.com"
    email2 = "dup2@example.com"
    username = "dup"
    password = "password"
    register_user(client, email1, username, password)
    r = register_user(client, email2, username, password)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in r.json()


def test_get_user(client: TestClient, fake_user: User) -> None:
    payload = client.get(f"{settings.API_V1_STR}/users/{fake_user.username}").json()
    assert payload["email"] == fake_user.email
    assert payload["username"] == fake_user.username


def test_get_not_existing_user(client: TestClient, database) -> None:
    response = client.get(f"{settings.API_V1_STR}/users/not_existing")
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
def test_update_user(client: TestClient, fake_auth, payload: dict) -> None:
    response = client.put(f"{settings.API_V1_STR}/users/settings", json=payload)
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
def test_update_user_not_modified(client: TestClient, fake_auth, payload: dict) -> None:
    response = client.put(f"{settings.API_V1_STR}/users/settings", json=payload)
    assert response.status_code == status.HTTP_304_NOT_MODIFIED

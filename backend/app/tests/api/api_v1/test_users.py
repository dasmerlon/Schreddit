from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


def register_user(client, email, username, password):
    payload = {"email": email, "username": username, "password": password}
    return client.post(f"{settings.API_V1_STR}/users/register", json=payload)


def test_register_user(client: TestClient) -> None:
    email = "test@example.com"
    username = "test"
    password = "password"
    r = register_user(client, email, username, password)
    assert r.status_code == status.HTTP_201_CREATED
    registered_user = r.json()

    assert registered_user["email"] == email
    assert registered_user["username"] == username


def test_register_existing_email(client: TestClient) -> None:
    email = "dup@example.com"
    username1 = "dup1"
    username2 = "dup2"
    password = "password"
    register_user(client, email, username1, password)
    r = register_user(client, email, username2, password)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in r.json()


def test_register_existing_username(client: TestClient) -> None:
    email1 = "dup1@example.com"
    email2 = "dup2@example.com"
    username = "dup"
    password = "password"
    register_user(client, email1, username, password)
    r = register_user(client, email2, username, password)
    assert r.status_code == 403
    assert "detail" in r.json()

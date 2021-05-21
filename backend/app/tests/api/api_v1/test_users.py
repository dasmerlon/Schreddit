from fastapi.testclient import TestClient

from app import models
from app.config import settings


def register_user(client, email, username, password):
    payload = {"email": email, "username": username, "password": password}
    return client.post(f"{settings.API_V1_STR}/users/register", json=payload)


def test_register_user(client: TestClient, database):
    email = "test@example.com"
    username = "test"
    password = "password"
    r = register_user(client, email, username, password)
    assert 200 <= r.status_code < 300
    registered_user = r.json()

    user = models.User.nodes.get(email=email, username=username)
    assert user
    assert user.email == registered_user["email"]
    assert user.username == registered_user["username"]


def test_register_existing_email(client: TestClient, database):
    register_user(client, "dup@example.com", "dup1", "password")
    r = register_user(client, "dup@example.com", "dup2", "password2")
    assert r.status_code == 403


def test_register_existing_username(client: TestClient, database):
    register_user(client, "dup1@example.com", "dup", "password")
    r = register_user(client, "dup2@example.com", "dup", "password2")
    assert r.status_code == 403

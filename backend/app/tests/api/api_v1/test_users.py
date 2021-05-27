from fastapi.testclient import TestClient

from app import crud, models
from app.core.config import settings


def register_user(client, email, username, password):
    payload = {"email": email, "username": username, "password": password}
    return client.post(f"{settings.API_V1_STR}/users/register", json=payload)


def test_register_user(client: TestClient, database) -> None:
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


def test_register_existing_email(client: TestClient, database) -> None:
    email = "dup@example.com"
    username1 = "dup1"
    username2 = "dup2"
    password = "password"
    register_user(client, email, username1, password)
    r = register_user(client, email, username2, password)
    assert r.status_code == 403

    user = crud.user.get_by_username(username2)
    assert user is None


def test_register_existing_username(client: TestClient, database) -> None:
    email1 = "dup1@example.com"
    email2 = "dup2@example.com"
    username = "dup"
    password = "password"
    register_user(client, email1, username, password)
    r = register_user(client, email2, username, password)
    assert r.status_code == 403

    user = crud.user.get_by_email(email2)
    assert user is None

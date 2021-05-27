from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient, database):
    email = "auth@example.com"
    username = "auth"
    password = "secure-password-1A§@ "

    payload_register = {"email": email, "username": username, "password": password}
    client.post(f"{settings.API_V1_STR}/users/register", json=payload_register)

    payload_login = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload_login)
    assert r.status_code == status.HTTP_200_OK

    access_token = r.json().get("access_token")
    assert access_token


def test_get_access_token_wrong_username(client: TestClient, database):
    payload_login = {"username": "adversary@example.com", "password": "password"}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload_login)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json().get("access_token") is None


def test_get_access_token_wrong_password(client: TestClient, database):
    email = "supersecure@example.com"
    username = "supersecure"
    password = "123456"

    payload_register = {"email": email, "username": username, "password": password}
    client.post(f"{settings.API_V1_STR}/users/register", json=payload_register)

    payload_login = {"username": "supersecure@example.com", "password": "12345"}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload_login)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json().get("access_token") is None

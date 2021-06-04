from fastapi import status
from fastapi.testclient import TestClient

from app import models, schemas
from app.core.config import settings


def test_get_access_token(
    client: TestClient,
    fake_schema_test_user_create: schemas.UserCreate,
    fake_test_user_in_db: models.User,
):
    payload = {
        "username": fake_schema_test_user_create.email,
        "password": fake_schema_test_user_create.password,
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert r.status_code == status.HTTP_200_OK

    access_token = r.json().get("access_token")
    assert access_token


def test_get_access_token_wrong_username(client: TestClient):
    payload_login = {"username": "adversary@example.com", "password": "password"}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload_login)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json().get("access_token") is None


def test_get_access_token_wrong_password(
    client: TestClient,
    fake_schema_test_user_create: schemas.UserCreate,
    fake_test_user_in_db: models.User,
):
    payload = {
        "username": fake_schema_test_user_create.email,
        "password": f"{fake_schema_test_user_create.password}wrong",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json().get("access_token") is None

from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import User
from app.tests.utils.fake_payloads import UserPayloads


def test_get_access_token(client: TestClient, test_user_in_db: User) -> None:
    payload = UserPayloads.get_auth()
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert r.status_code == status.HTTP_200_OK

    access_token = r.json().get("access_token")
    assert access_token


def test_get_access_token_wrong_username(
    client: TestClient, test_user_in_db: User
) -> None:
    payload = UserPayloads.get_auth()
    payload["username"] = "adversary@example.com"
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json().get("access_token") is None


def test_get_access_token_wrong_password(
    client: TestClient, test_user_in_db: User
) -> None:
    payload = UserPayloads.get_auth()
    payload["password"] += "wrong"
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json().get("access_token") is None

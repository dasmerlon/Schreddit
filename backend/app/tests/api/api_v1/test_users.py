import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import crud, models, schemas
from app.core.config import settings
from app.core.security import verify_password


def register_user(client, email, username, password):
    payload = {"email": email, "username": username, "password": password}
    return client.post(f"{settings.API_V1_STR}/users/register", json=payload)


def test_register_user(
    client: TestClient, fake_schema_user_create: schemas.UserCreate, remove_user
) -> None:
    payload = fake_schema_user_create.dict()
    r = client.post(f"{settings.API_V1_STR}/users/register", json=payload)
    registered_user = r.json()
    remove_user(registered_user["uid"])
    assert r.status_code == status.HTTP_201_CREATED
    assert registered_user["email"] == fake_schema_user_create.email
    assert registered_user["username"] == fake_schema_user_create.username


def test_register_existing_email(
    client: TestClient,
    fake_test_user_in_db: models.User,
    fake_schema_test_user_create: schemas.UserCreate,
) -> None:
    payload = fake_schema_test_user_create.dict()
    payload["username"] = "newuser-samemail"
    r = client.post(f"{settings.API_V1_STR}/users/register", json=payload)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in r.json()


def test_register_existing_username(
    client: TestClient,
    fake_test_user_in_db: models.User,
    fake_schema_test_user_create: schemas.UserCreate,
) -> None:
    payload = fake_schema_test_user_create.dict()
    payload["email"] = "newmail@sameuser.com"
    r = client.post(f"{settings.API_V1_STR}/users/register", json=payload)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in r.json()


def test_get_user(client: TestClient, fake_random_user_in_db: models.User) -> None:
    payload = client.get(
        f"{settings.API_V1_STR}/users/{fake_random_user_in_db.username}"
    ).json()
    assert payload["email"] == fake_random_user_in_db.email
    assert payload["username"] == fake_random_user_in_db.username


def test_get_not_existing_user(client: TestClient) -> None:
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
def test_update_user(
    client: TestClient, fake_test_user_auth: models.User, payload: dict
) -> None:
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
def test_update_user_not_modified(
    client: TestClient, fake_test_user_auth: models.User, payload: dict
) -> None:
    response = client.put(f"{settings.API_V1_STR}/users/settings", json=payload)
    assert response.status_code == status.HTTP_304_NOT_MODIFIED

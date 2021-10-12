from typing import List

from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import Subreddit, User
from app.tests.utils.fake_payloads import SubredditPayloads


def test_get_subreddit(client: TestClient, subreddit_in_db: Subreddit) -> None:
    subreddit = subreddit_in_db
    r = client.get(f"{settings.API_V1_STR}/r/{subreddit.sr}")
    assert r.status_code == status.HTTP_200_OK
    sr = r.json()
    assert sr
    assert sr["sr"] == subreddit.sr


def test_get_subreddit_fail(client: TestClient, subreddit_in_db: Subreddit) -> None:
    r = client.get(f"{settings.API_V1_STR}/r/does_not_exist")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


def test_create_subreddit(
    client: TestClient, fake_auth: User, remove_subreddits: List
) -> None:
    payload = SubredditPayloads.get_create(type="public")
    r = client.post(f"{settings.API_V1_STR}/r", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    created_subreddit = r.json()
    assert created_subreddit
    assert created_subreddit.get("sr")
    assert "detail" not in created_subreddit
    remove_subreddits.append(created_subreddit["uid"])

    assert created_subreddit["admin"]["email"] == fake_auth.email
    assert created_subreddit["admin"]["username"] == fake_auth.username
    assert created_subreddit["sr"] == payload["sr"]

    r = client.get(f"{settings.API_V1_STR}/r/{created_subreddit['sr']}")
    assert r.status_code == status.HTTP_200_OK
    retrieved_subreddit = r.json()
    assert retrieved_subreddit
    assert retrieved_subreddit.get("sr")
    assert "detail" not in created_subreddit

    assert retrieved_subreddit["admin"]["email"] == fake_auth.email
    assert retrieved_subreddit["admin"]["username"] == fake_auth.username
    assert retrieved_subreddit["sr"] == payload["sr"]


def test_create_subreddit_existing_sr(
    client: TestClient, fake_auth: User, subreddit_in_db: Subreddit
) -> None:
    payload = SubredditPayloads.get_create(type="public")
    r = client.post(f"{settings.API_V1_STR}/r", json=payload)
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_create_subreddit_user_not_logged_in(client: TestClient) -> None:
    payload = SubredditPayloads.get_create(type="public")
    r = client.post(f"{settings.API_V1_STR}/r", json=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_subreddit_wrong_type(client: TestClient, fake_auth: User) -> None:
    payload = SubredditPayloads.get_create(type="public")
    payload["type"] = ""
    r = client.post(f"{settings.API_V1_STR}/r", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in r.json()

    payload["type"] = "publikkkk"
    r = client.post(f"{settings.API_V1_STR}/r", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in r.json()


def test_update_subreddit_type_private(
    client: TestClient, fake_auth: User, subreddit_private_in_db: Subreddit
) -> None:
    subreddit = subreddit_private_in_db
    payload = SubredditPayloads.get_update(type="private")
    r = client.put(f"{settings.API_V1_STR}/r/{subreddit.sr}", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/r/{subreddit.sr}")
    assert r.status_code == status.HTTP_200_OK
    retrieved_subreddit = r.json()
    assert retrieved_subreddit
    assert retrieved_subreddit.get("sr")
    assert "detail" not in retrieved_subreddit
    assert retrieved_subreddit["created_at"] != retrieved_subreddit["updated_at"]

    for key in payload:
        assert retrieved_subreddit[key] == payload[key]


def test_update_subreddit_type_private_fail(
    client: TestClient, fake_auth: User, subreddit_private_in_db: Subreddit
) -> None:
    payload = SubredditPayloads.get_update(type="private")
    r = client.put(f"{settings.API_V1_STR}/r/does_not_exist", json=payload)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


def test_update_subreddit_from_other_user_fail(
    client: TestClient,
    fake_auth: User,
    subreddit_in_db_other_user: Subreddit,
) -> None:
    subreddit = subreddit_in_db_other_user
    payload = SubredditPayloads.get_update(type="private")
    r = client.put(f"{settings.API_V1_STR}/r/{subreddit.sr}", json=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in r.json()


def test_update_subreddit_not_modified(
    client: TestClient, fake_auth: User, subreddit_in_db: Subreddit
) -> None:
    payload = SubredditPayloads.get_create(type="public")
    r = client.put(f"{settings.API_V1_STR}/r/{payload['sr']}", json=payload)
    assert r.status_code == status.HTTP_304_NOT_MODIFIED

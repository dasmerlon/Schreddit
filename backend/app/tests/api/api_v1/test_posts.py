from typing import Dict, List
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import Post, User
from app.tests.utils.fake_payloads import PostPayloads


def test_get_post(client: TestClient, post_self_in_db: Post) -> None:
    r = client.get(f"{settings.API_V1_STR}/posts/{post_self_in_db.uid}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    assert post["uid"].replace("-", "") == post_self_in_db.uid


def test_get_post_fail(client: TestClient, post_self_in_db: Post) -> None:
    r = client.get(f"{settings.API_V1_STR}/posts/{uuid4().hex}")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


@pytest.mark.parametrize(
    "payload",
    [PostPayloads.get_create(type="link"), PostPayloads.get_create(type="self")],
)
def test_submit_post(
    client: TestClient,
    fake_auth: User,
    payload: Dict,
    remove_posts: List,
) -> None:
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    created_post = r.json()
    remove_posts.append(created_post["uid"])
    assert r.status_code == status.HTTP_201_CREATED

    for key in payload:
        if key != "sr":  # subreddit must be asserted separately
            assert created_post[key] == payload[key]
    assert created_post["author"]["email"] == fake_auth.email
    assert created_post["author"]["username"] == fake_auth.username
    # TODO: assert subreddit name is correct, also in test cases below

    r = client.get(f"{settings.API_V1_STR}/posts/{created_post['uid']}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    for key in payload:
        if key != "sr":
            assert post[key] == payload[key]


@pytest.mark.parametrize(
    "payload",
    [
        PostPayloads.get_create(type="link", valid=False),
        PostPayloads.get_create(type="self", valid=False),
    ],
)
def test_submit_post_fail(client: TestClient, fake_auth: User, payload: Dict) -> None:
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_update_post_type_self(
    client: TestClient,
    fake_auth: User,
    post_self_in_db: Post,
) -> None:
    payload = PostPayloads.get_update(type="self")
    r = client.put(f"{settings.API_V1_STR}/posts/{post_self_in_db.uid}", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/posts/{post_self_in_db.uid}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    assert post["created_at"] != post["updated_at"]
    for key in payload:
        assert post[key] == payload[key]


def test_update_post_type_self_fail(
    client: TestClient,
    fake_auth: User,
    post_self_in_db: Post,
) -> None:
    payload = PostPayloads.get_update(type="self")
    r = client.put(f"{settings.API_V1_STR}/posts/{uuid4().hex}", json=payload)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()

    r = client.get(f"{settings.API_V1_STR}/posts/{post_self_in_db.uid}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    for key in payload:
        assert post[key] == getattr(post_self_in_db, key)


def test_update_post_type_self_fail_url(
    client: TestClient,
    fake_auth: User,
    post_self_in_db: Post,
) -> None:
    payload = PostPayloads.get_update(type="self", valid=False)
    r = client.put(f"{settings.API_V1_STR}/posts/{post_self_in_db.uid}", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()

    r = client.get(f"{settings.API_V1_STR}/posts/{post_self_in_db.uid}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    for key in payload:
        assert post[key] == getattr(post_self_in_db, key)


def test_update_post_type_link(
    client: TestClient,
    fake_auth: User,
    post_link_in_db: Post,
) -> None:
    payload = PostPayloads.get_update(type="link")
    r = client.put(f"{settings.API_V1_STR}/posts/{post_link_in_db.uid}", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/posts/{post_link_in_db.uid}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    assert post["created_at"] != post["updated_at"]
    for key in payload:
        assert post[key] == payload[key]


def test_update_post_type_link_fail_text(
    client: TestClient,
    fake_auth: User,
    post_link_in_db: Post,
) -> None:
    payload = PostPayloads.get_update(type="link", valid=False)
    r = client.put(f"{settings.API_V1_STR}/posts/{post_link_in_db.uid}", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()

    r = client.get(f"{settings.API_V1_STR}/posts/{post_link_in_db.uid}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    for key in payload:
        assert post[key] == getattr(post_link_in_db, key)

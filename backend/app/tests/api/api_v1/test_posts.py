from typing import Dict, List, Tuple
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import PostContent, PostMeta, Subreddit, User
from app.schemas import PostSort
from app.tests.utils.fake_payloads import PostPayloads


def test_get_post(client: TestClient, post_self_in_db: (PostMeta, PostContent)) -> None:
    metadata = post_self_in_db[0]
    r = client.get(f"{settings.API_V1_STR}/posts/{metadata.uid}")
    assert r.status_code == status.HTTP_200_OK
    post = r.json()
    assert post
    assert post["metadata"]["uid"].replace("-", "") == metadata.uid


def test_get_post_fail(
    client: TestClient, post_self_in_db: (PostMeta, PostContent)
) -> None:
    r = client.get(f"{settings.API_V1_STR}/posts/{uuid4().hex}")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


@pytest.mark.parametrize("sort", [PostSort.new, PostSort.top, PostSort.hot])
def test_get_posts_auth(
    client: TestClient,
    fake_auth: User,
    sort: PostSort,
    posts_with_votes_in_db: List[Tuple[PostMeta, PostContent]],
    subreddit_in_db: Subreddit,
) -> None:
    r = client.get(f"{settings.API_V1_STR}/posts/list?sr={subreddit_in_db.sr}")
    assert r.status_code == status.HTTP_200_OK
    post_list = r.json()
    for post in post_list["data"]:
        assert post["metadata"]["uid"].replace("-", "") in [
            post[0].uid for post in posts_with_votes_in_db
        ]


def test_get_posts_empty_subreddit(
    client: TestClient, fake_auth: User, subreddit_in_db: Subreddit
) -> None:
    r = client.get(f"{settings.API_V1_STR}/posts/list?sr={subreddit_in_db.sr}")
    assert r.status_code == status.HTTP_200_OK
    post_list = r.json()
    assert not post_list["data"]
    assert post_list["links"]["prev"] is None
    assert post_list["links"]["next"] is None


@pytest.mark.parametrize(
    "payload",
    [PostPayloads.get_create(type="link"), PostPayloads.get_create(type="self")],
)
def test_submit_post(
    client: TestClient,
    fake_auth: User,
    payload: Dict,
    subreddit_in_db: Subreddit,
    remove_posts: List,
) -> None:
    metadata = payload["metadata"]
    content = payload["content"]
    metadata["sr"] = subreddit_in_db.sr
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    created_post = r.json()
    assert created_post
    assert created_post.get("metadata")
    assert created_post.get("content")
    remove_posts.append(created_post["metadata"]["uid"])

    for key in metadata:
        if key != "sr":
            assert created_post["metadata"][key] == metadata[key]
    for key in content:
        assert created_post["content"][key] == content[key]
    assert created_post["metadata"]["author"] == fake_auth.username
    assert created_post["metadata"]["sr"] == metadata["sr"]

    r = client.get(f"{settings.API_V1_STR}/posts/{created_post['metadata']['uid']}")
    assert r.status_code == status.HTTP_200_OK
    retrieved_post = r.json()
    assert retrieved_post
    assert retrieved_post.get("metadata")
    assert retrieved_post.get("content")

    for key in metadata:
        if key != "sr":
            assert retrieved_post["metadata"][key] == metadata[key]
    for key in content:
        assert retrieved_post["content"][key] == content[key]
    assert retrieved_post["metadata"]["author"] == fake_auth.username
    assert retrieved_post["metadata"]["sr"] == metadata["sr"]


@pytest.mark.parametrize(
    "payload",
    [
        PostPayloads.get_create(type="link", valid=False),
        PostPayloads.get_create(type="self", valid=False),
    ],
)
def test_submit_post_wrong_format(
    client: TestClient, fake_auth: User, payload: Dict, subreddit_in_db: Subreddit
) -> None:
    payload["metadata"]["sr"] = subreddit_in_db.sr
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in r.json()


@pytest.mark.parametrize(
    "payload",
    [PostPayloads.get_create(type="link"), PostPayloads.get_create(type="self")],
)
def test_submit_post_empty_title(
    client: TestClient, fake_auth: User, payload: Dict, subreddit_in_db: Subreddit
) -> None:
    payload["metadata"]["sr"] = subreddit_in_db.sr
    payload["content"]["title"] = "  "
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in r.json()


def test_update_post_type_self(
    client: TestClient,
    fake_auth: User,
    post_self_in_db: (PostMeta, PostContent),
) -> None:
    metadata = post_self_in_db[0]
    payload = PostPayloads.get_update(type="self")
    r = client.put(f"{settings.API_V1_STR}/posts/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/posts/{metadata.uid}")
    assert r.status_code == status.HTTP_200_OK
    retrieved_post = r.json()
    assert retrieved_post
    assert retrieved_post.get("metadata")
    assert retrieved_post.get("content")
    assert (
        retrieved_post["metadata"]["created_at"]
        != retrieved_post["metadata"]["updated_at"]
    )

    for key in payload["metadata"]:
        if key != "sr":
            assert retrieved_post["metadata"][key] == payload["metadata"][key]
    for key in payload["content"]:
        assert retrieved_post["content"][key] == payload["content"][key]


def test_update_post_type_self_fail(
    client: TestClient,
    fake_auth: User,
    post_self_in_db: (PostMeta, PostContent),
) -> None:
    payload = PostPayloads.get_update(type="self")
    r = client.put(f"{settings.API_V1_STR}/posts/{uuid4().hex}", json=payload)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


def test_update_post_type_self_fail_url(
    client: TestClient,
    fake_auth: User,
    post_self_in_db: (PostMeta, PostContent),
) -> None:
    metadata = post_self_in_db[0]
    payload = PostPayloads.get_update(type="self", valid=False)
    r = client.put(f"{settings.API_V1_STR}/posts/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_update_post_type_link(
    client: TestClient,
    fake_auth: User,
    post_link_in_db: (PostMeta, PostContent),
) -> None:
    metadata = post_link_in_db[0]
    payload = PostPayloads.get_update(type="link")
    r = client.put(f"{settings.API_V1_STR}/posts/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/posts/{metadata.uid}")
    assert r.status_code == status.HTTP_200_OK
    retrieved_post = r.json()
    assert retrieved_post
    assert retrieved_post.get("metadata")
    assert retrieved_post.get("content")
    assert (
        retrieved_post["metadata"]["created_at"]
        != retrieved_post["metadata"]["updated_at"]
    )

    for key in payload["metadata"]:
        if key != "sr":
            assert retrieved_post["metadata"][key] == payload["metadata"][key]
    for key in payload["content"]:
        assert retrieved_post["content"][key] == payload["content"][key]


def test_update_post_type_link_fail_text(
    client: TestClient,
    fake_auth: User,
    post_link_in_db: (PostMeta, PostContent),
) -> None:
    metadata = post_link_in_db[0]
    payload = PostPayloads.get_update(type="link", valid=False)
    r = client.put(f"{settings.API_V1_STR}/posts/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_update_post_from_other_user_fail(
    client: TestClient,
    fake_auth: User,
    post_self_in_db_other_user: (PostMeta, PostContent),
) -> None:
    metadata = post_self_in_db_other_user[0]
    payload = PostPayloads.get_update(type="self")
    r = client.put(f"{settings.API_V1_STR}/posts/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in r.json()


@pytest.mark.parametrize(
    "payload",
    [PostPayloads.get_update(type="link"), PostPayloads.get_update(type="self")],
)
def test_update_post_empty_title(
    client: TestClient,
    fake_auth: User,
    payload: Dict,
    post_link_in_db: (PostMeta, PostContent),
) -> None:
    metadata = post_link_in_db[0]
    payload["content"]["title"] = "  "
    r = client.put(f"{settings.API_V1_STR}/posts/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in r.json()

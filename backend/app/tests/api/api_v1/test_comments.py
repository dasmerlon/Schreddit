from typing import List, Union
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import (CommentContent, CommentMeta, PostContent, PostMeta,
                        Subreddit, User)
from app.tests.utils.fake_payloads import CommentPayloads


def test_get_comment(
    client: TestClient, comment_in_db: (CommentMeta, CommentContent)
) -> None:
    metadata = comment_in_db[0]
    r = client.get(f"{settings.API_V1_STR}/comments/{metadata.uid}")
    assert r.status_code == status.HTTP_200_OK
    comment = r.json()
    assert comment
    assert comment["metadata"]["uid"].replace("-", "") == metadata.uid


def test_get_comment_fail(
    client: TestClient, comment_in_db: (CommentMeta, CommentContent)
) -> None:
    r = client.get(f"{settings.API_V1_STR}/comments/{uuid4().hex}")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


@pytest.mark.parametrize("type", ["post", "comment"])
def test_submit_comment(
    client: TestClient,
    fake_auth: User,
    type: str,
    comment_in_db: (CommentMeta, CommentContent),
    post_self_in_db: (PostMeta, PostContent),
    remove_comments: List,
) -> None:
    payload = CommentPayloads.get_create()
    if type == "post":
        parent = post_self_in_db[0]
    elif type == "comment":
        parent = comment_in_db[0]

    r = client.post(f"{settings.API_V1_STR}/comments/{parent.uid}", json=payload)

    # assert post creation
    assert r.status_code == status.HTTP_201_CREATED
    created_comment = r.json()
    assert created_comment
    assert created_comment.get("metadata")
    assert created_comment.get("content")
    remove_comments.append(created_comment["metadata"]["uid"])
    assert created_comment["content"]["text"] == payload["content"]["text"]
    assert created_comment["metadata"]["author"] == fake_auth.username
    assert created_comment["metadata"]["parent"].replace("-", "") == parent.uid

    r = client.get(
        f"{settings.API_V1_STR}/comments/{created_comment['metadata']['uid']}"
    )
    assert r.status_code == status.HTTP_200_OK
    retrieved_comment = r.json()
    assert retrieved_comment
    assert retrieved_comment.get("metadata")
    assert retrieved_comment.get("content")
    assert retrieved_comment["content"]["text"] == payload["content"]["text"]
    assert retrieved_comment["metadata"]["author"] == fake_auth.username
    assert retrieved_comment["metadata"]["parent"].replace("-", "") == parent.uid


@pytest.mark.parametrize("type", ["post", "comment"])
def test_submit_comment_nonexisting_parent(
    client: TestClient, fake_auth: User, type: str, subreddit_in_db: Subreddit
) -> None:
    payload = CommentPayloads.get_create()
    r = client.post(f"{settings.API_V1_STR}/comments/{uuid4().hex}", json=payload)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


@pytest.mark.parametrize("text", ["  ", None])
def test_submit_comment_wrong_format(
    client: TestClient,
    fake_auth: User,
    text: Union[str, None],
    post_self_in_db: (PostMeta, PostContent),
) -> None:
    payload = CommentPayloads.get_create()
    payload["content"]["text"] = text
    parent = post_self_in_db[0]
    r = client.post(f"{settings.API_V1_STR}/comments/{parent.uid}", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in r.json()


def test_update_comment(
    client: TestClient,
    fake_auth: User,
    comment_in_db: (CommentMeta, CommentContent),
) -> None:
    metadata = comment_in_db[0]
    payload = CommentPayloads.get_update()
    r = client.put(f"{settings.API_V1_STR}/comments/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/comments/{metadata.uid}")
    assert r.status_code == status.HTTP_200_OK
    retrieved_comment = r.json()
    assert retrieved_comment
    assert retrieved_comment.get("metadata")
    assert retrieved_comment.get("content")
    assert (
        retrieved_comment["metadata"]["created_at"]
        != retrieved_comment["metadata"]["updated_at"]
    )
    assert retrieved_comment["content"]["text"] == payload["content"]["text"]


def test_update_comment_nonexisting_parent(
    client: TestClient,
    fake_auth: User,
    comment_in_db: (CommentMeta, CommentContent),
) -> None:
    payload = CommentPayloads.get_update()
    r = client.put(f"{settings.API_V1_STR}/comments/{uuid4().hex}", json=payload)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()


@pytest.mark.parametrize("text", ["  ", None])
def test_update_comment_wrong_format(
    client: TestClient,
    fake_auth: User,
    text: Union[str, None],
    comment_in_db: (CommentMeta, CommentContent),
) -> None:
    metadata = comment_in_db[0]
    payload = CommentPayloads.get_update()
    payload["content"]["text"] = text
    r = client.put(f"{settings.API_V1_STR}/comments/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in r.json()


def test_update_comment_from_other_user(
    client: TestClient,
    fake_auth: User,
    comment_in_db_other_user: (CommentMeta, CommentContent),
) -> None:
    metadata = comment_in_db_other_user[0]
    payload = CommentPayloads.get_update()
    r = client.put(f"{settings.API_V1_STR}/comments/{metadata.uid}", json=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in r.json()

from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import CommentContent, CommentMeta, PostContent, PostMeta, User


@pytest.mark.parametrize("dir", [1, -1])
@pytest.mark.parametrize("type", ["post", "comment"])
def test_vote(
    client: TestClient,
    fake_auth: User,
    comment_in_db_other_user: (CommentMeta, CommentContent),
    post_self_in_db_other_user: (PostMeta, PostContent),
    dir: int,
    type: str,
) -> None:
    if type == "post":
        metadata = post_self_in_db_other_user[0]
    elif type == "comment":
        metadata = comment_in_db_other_user[0]
    r = client.put(f"{settings.API_V1_STR}/vote/{metadata.uid}/{dir}")
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/state")
    assert r.status_code == status.HTTP_200_OK
    state = r.json()
    assert state == dir

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/count")
    assert r.status_code == status.HTTP_200_OK
    count = r.json()
    assert count == dir


@pytest.mark.parametrize("type", ["post", "comment"])
def test_upvote_already_upvoted(
    client: TestClient,
    fake_auth: User,
    comment_in_db_upvoted: (CommentMeta, CommentContent),
    post_self_in_db_upvoted: (PostMeta, PostContent),
    type: str,
) -> None:
    if type == "post":
        metadata = post_self_in_db_upvoted[0]
    elif type == "comment":
        metadata = comment_in_db_upvoted[0]
    r = client.put(f"{settings.API_V1_STR}/vote/{metadata.uid}/1")
    assert r.status_code == status.HTTP_304_NOT_MODIFIED

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/state")
    assert r.status_code == status.HTTP_200_OK
    state = r.json()
    assert state == 1

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/count")
    assert r.status_code == status.HTTP_200_OK
    count = r.json()
    assert count == 1


@pytest.mark.parametrize("type", ["post", "comment"])
def test_remove_vote(
    client: TestClient,
    fake_auth: User,
    comment_in_db_upvoted: (CommentMeta, CommentContent),
    post_self_in_db_upvoted: (PostMeta, PostContent),
    type: str,
) -> None:
    if type == "post":
        metadata = post_self_in_db_upvoted[0]
    elif type == "comment":
        metadata = comment_in_db_upvoted[0]
    r = client.put(f"{settings.API_V1_STR}/vote/{metadata.uid}/0")
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/state")
    assert r.status_code == status.HTTP_200_OK
    state = r.json()
    assert state == 0

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/count")
    assert r.status_code == status.HTTP_200_OK
    count = r.json()
    assert count == 0


@pytest.mark.parametrize("dir", [1, -1])
@pytest.mark.parametrize("type", ["post", "comment"])
def test_vote_nonexisting_thing(
    client: TestClient,
    fake_auth: User,
    comment_in_db_other_user: (CommentMeta, CommentContent),
    post_self_in_db_other_user: (PostMeta, PostContent),
    dir: int,
    type: str,
) -> None:
    if type == "post":
        metadata = post_self_in_db_other_user[0]
    elif type == "comment":
        metadata = comment_in_db_other_user[0]
    r = client.put(f"{settings.API_V1_STR}/vote/{uuid4()}/{dir}")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in r.json()

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/state")
    assert r.status_code == status.HTTP_200_OK
    state = r.json()
    assert state == 0

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/count")
    assert r.status_code == status.HTTP_200_OK
    count = r.json()
    assert count == 0


@pytest.mark.parametrize("type", ["post", "comment"])
def test_get_vote_count_nonexisting_thing(
    client: TestClient,
    fake_auth: User,
    comment_in_db_other_user: (CommentMeta, CommentContent),
    post_self_in_db_other_user: (PostMeta, PostContent),
    type: str,
) -> None:
    if type == "post":
        metadata = post_self_in_db_other_user[0]
    elif type == "comment":
        metadata = comment_in_db_other_user[0]
    r = client.get(f"{settings.API_V1_STR}/vote/{uuid4()}/count")
    assert r.status_code == status.HTTP_404_NOT_FOUND

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/state")
    assert r.status_code == status.HTTP_200_OK
    state = r.json()
    assert state == 0

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/count")
    assert r.status_code == status.HTTP_200_OK
    count = r.json()
    assert count == 0


@pytest.mark.parametrize("type", ["post", "comment"])
def test_get_vote_state_nonexisting_thing(
    client: TestClient,
    fake_auth: User,
    comment_in_db_other_user: (CommentMeta, CommentContent),
    post_self_in_db_other_user: (PostMeta, PostContent),
    type: str,
) -> None:
    if type == "post":
        metadata = post_self_in_db_other_user[0]
    elif type == "comment":
        metadata = comment_in_db_other_user[0]
    r = client.get(f"{settings.API_V1_STR}/vote/{uuid4()}/state")
    assert r.status_code == status.HTTP_404_NOT_FOUND

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/state")
    assert r.status_code == status.HTTP_200_OK
    state = r.json()
    assert state == 0

    r = client.get(f"{settings.API_V1_STR}/vote/{metadata.uid}/count")
    assert r.status_code == status.HTTP_200_OK
    count = r.json()
    assert count == 0

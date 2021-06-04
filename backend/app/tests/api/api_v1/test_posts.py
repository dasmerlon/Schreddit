from fastapi import status
from fastapi.testclient import TestClient

from app import models, schemas
from app.core.config import settings


def test_submit_post_type_link(
    client: TestClient,
    fake_test_user_auth,
    fake_schema_post_create_link: schemas.PostCreate,
    remove_post,
) -> None:
    payload = fake_schema_post_create_link.dict()
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    created_post = r.json()
    remove_post(created_post["uid"])
    assert r.status_code == status.HTTP_201_CREATED

    for key in payload:
        if key != "sr":  # subreddit must be asserted separately
            assert created_post[key] == payload[key]
    assert created_post["author"]["email"] == fake_test_user_auth.email
    assert created_post["author"]["username"] == fake_test_user_auth.username
    # TODO: assert subreddit name is correct, also in test cases below


def test_submit_post_type_link_fail(
    client: TestClient,
    fake_test_user_auth,
    fake_schema_post_create_link: schemas.PostCreate,
) -> None:
    payload = fake_schema_post_create_link.dict()
    payload["text"] = "Lorem ipsum"
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_submit_post_type_self(
    client: TestClient,
    fake_test_user_auth,
    fake_schema_post_create_self: schemas.PostCreate,
    remove_post,
) -> None:
    payload = fake_schema_post_create_self.dict()
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    created_post = r.json()
    remove_post(created_post["uid"])
    assert r.status_code == status.HTTP_201_CREATED

    for key in payload:
        if key != "sr":  # subreddit must be asserted separately
            assert created_post[key] == payload[key]
    assert created_post["author"]["email"] == fake_test_user_auth.email
    assert created_post["author"]["username"] == fake_test_user_auth.username


def test_submit_post_type_self_fail(
    client: TestClient,
    fake_test_user_auth,
    fake_schema_post_create_self: schemas.PostCreate,
) -> None:
    payload = fake_schema_post_create_self.dict()
    payload["url"] = "https://www.google.com/"
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_update_post_type_self(
    client: TestClient,
    fake_test_user_auth,
    fake_self_post_in_db: models.Post,
    fake_schema_post_update_self: schemas.PostUpdate,
) -> None:
    payload = fake_schema_post_update_self.dict()
    payload["uid"] = fake_self_post_in_db.uid
    r = client.put(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_update_post_type_self_fail_uid(
    client: TestClient,
    fake_test_user_auth,
    fake_self_post_in_db: models.Post,
    fake_schema_post_update_self: schemas.PostUpdate,
) -> None:
    payload = fake_schema_post_update_self.dict()
    r = client.put(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_update_post_type_self_fail_url(
    client: TestClient,
    fake_test_user_auth,
    fake_self_post_in_db: models.Post,
    fake_schema_post_update_self: schemas.PostUpdate,
) -> None:
    payload = fake_schema_post_update_self.dict()
    payload["uid"] = fake_self_post_in_db.uid
    payload["url"] = "https://www.google.com/"
    r = client.put(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_update_post_type_link(
    client: TestClient,
    fake_test_user_auth,
    fake_link_post_in_db: models.Post,
    fake_schema_post_update_link: schemas.PostUpdate,
) -> None:
    payload = fake_schema_post_update_link.dict()
    payload["uid"] = fake_link_post_in_db.uid
    r = client.put(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_update_post_type_link_fail_text(
    client: TestClient,
    fake_test_user_auth,
    fake_link_post_in_db: models.Post,
    fake_schema_post_update_link: schemas.PostUpdate,
) -> None:
    payload = fake_schema_post_update_link.dict()
    payload["text"] = "Lorem ipsum"
    payload["uid"] = fake_link_post_in_db.uid
    r = client.put(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()

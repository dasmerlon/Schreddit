from fastapi import status
from fastapi.testclient import TestClient

from app import models
from app.core.config import settings


def test_submit_post_type_link(client: TestClient, fake_auth: models.User) -> None:
    payload = {
        "nsfw": False,
        "spoiler": True,
        "sr": "testsub",
        "title": "Posting a link",
        "type": "link",
        "url": "https://www.google.de/",
    }
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    created_post = r.json()

    for key in payload:
        if key != "sr":  # subreddit must be asserted separately
            assert created_post[key] == payload[key]
    assert created_post["author"]["email"] == fake_auth.email
    assert created_post["author"]["username"] == fake_auth.username
    # TODO: assert subreddit name is correct, also in test cases below


def test_submit_post_type_link_fail(client: TestClient, fake_auth: models.User) -> None:
    payload = {
        "nsfw": False,
        "spoiler": True,
        "sr": "testsub",
        "text": "Lorem ipsum",
        "title": "Posting a link",
        "type": "link",
        "url": "https://www.google.de/",
    }
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()


def test_submit_post_type_self(client: TestClient, fake_auth: models.User) -> None:
    payload = {
        "nsfw": True,
        "spoiler": False,
        "sr": "testsub",
        "text": "Lorem ipsum",
        "title": "Self post",
        "type": "self",
    }
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    created_post = r.json()

    for key in payload:
        if key != "sr":  # subreddit must be asserted separately
            assert created_post[key] == payload[key]
    assert created_post["author"]["email"] == fake_auth.email
    assert created_post["author"]["username"] == fake_auth.username


def test_submit_post_type_self_fail(client: TestClient, fake_auth: models.User) -> None:
    payload = {
        "nsfw": False,
        "spoiler": True,
        "sr": "testsub",
        "text": "Lorem ipsum",
        "title": "Self post",
        "type": "self",
        "url": "https://www.google.de/",
    }
    r = client.post(f"{settings.API_V1_STR}/posts", json=payload)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in r.json()

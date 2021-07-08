import pytest
from pydantic import UUID4

from app import crud
from app.models import Post, Subreddit, User
from app.tests.utils.fake_schemas import (PostSchemas, SubredditSchemas,
                                          UserSchemas)

"""
Fixtures for the test user
"""


@pytest.fixture
def test_user_in_db() -> User:
    user = crud.user.create(UserSchemas.get_create())
    yield user
    crud.user.remove(user.uid)


@pytest.fixture
def post_link_in_db(test_user_in_db: User, subreddit_in_db: Subreddit) -> Post:
    post = crud.post.create(PostSchemas.get_create(type="link"))
    crud.post.set_author(post, test_user_in_db)
    crud.post.set_subreddit(post, subreddit_in_db)
    yield post
    crud.post.remove(post.uid)


@pytest.fixture
def post_self_in_db(test_user_in_db: User, subreddit_in_db: Subreddit) -> Post:
    post = crud.post.create(PostSchemas.get_create(type="self"))
    crud.post.set_author(post, test_user_in_db)
    crud.post.set_subreddit(post, subreddit_in_db)
    yield post
    crud.post.remove(post.uid)


@pytest.fixture
def subreddit_in_db(test_user_in_db: User) -> Subreddit:
    sr = crud.subreddit.create(SubredditSchemas.get_create(type="public"))
    crud.subreddit.set_admin(sr, test_user_in_db)
    yield sr
    crud.subreddit.remove(sr.uid)


"""
Fixtures for removing users and posts
"""


@pytest.fixture
def remove_users():
    uids = []
    yield uids
    for uid in uids:
        if crud.user.get(UUID4(uid)) is not None:
            crud.user.remove(UUID4(uid))


@pytest.fixture
def remove_posts():
    uids = []
    yield uids
    for uid in uids:
        if crud.post.get(UUID4(uid)) is not None:
            crud.post.remove(UUID4(uid))

import pytest
from pydantic import UUID4

from app import crud
from app.models import PostMeta, Subreddit, User
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
def post_link_in_db(test_user_in_db: User, subreddit_in_db: Subreddit) -> PostMeta:
    schema = PostSchemas.get_create(type="link")
    post_meta = crud.post_meta.create(schema.metadata)
    post_content = crud.post_content.create(post_meta.uid, schema.content)
    crud.post_meta.set_author(post_meta, test_user_in_db)
    crud.post_meta.set_subreddit(post_meta, subreddit_in_db)
    yield post_meta, post_content
    crud.post_meta.remove(post_meta.uid)
    crud.post_content.remove(post_meta.uid)


@pytest.fixture
def post_self_in_db(test_user_in_db: User, subreddit_in_db: Subreddit) -> PostMeta:
    schema = PostSchemas.get_create(type="self")
    post_meta = crud.post_meta.create(schema.metadata)
    post_content = crud.post_content.create(post_meta.uid, schema.content)
    crud.post_meta.set_author(post_meta, test_user_in_db)
    crud.post_meta.set_subreddit(post_meta, subreddit_in_db)
    yield post_meta, post_content
    crud.post_meta.remove(post_meta.uid)
    crud.post_content.remove(post_meta.uid)


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
        if crud.post_meta.get(UUID4(uid)) is not None:
            crud.post_meta.remove(UUID4(uid))
        if crud.post_content.get(UUID4(uid)) is not None:
            crud.post_content.remove(UUID4(uid))

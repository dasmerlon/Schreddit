import pytest
from pydantic import UUID4

from app import crud
from app.models import Post, User
from app.tests.utils.fake_schemas import PostSchemas, UserSchemas

"""
Fixtures for the test user
"""


@pytest.fixture
def test_user_in_db() -> User:
    user = crud.user.create(UserSchemas.get_create())
    yield user
    crud.user.remove(user.uid)


@pytest.fixture
def post_link_in_db(test_user_in_db: User) -> Post:
    post = crud.post.create(PostSchemas.get_create(type="link"), test_user_in_db)
    yield post
    crud.post.remove(post.uid)


@pytest.fixture
def post_self_in_db(request, test_user_in_db: User) -> Post:
    post = crud.post.create(PostSchemas.get_create(type="self"), test_user_in_db)
    yield post
    crud.post.remove(post.uid)


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

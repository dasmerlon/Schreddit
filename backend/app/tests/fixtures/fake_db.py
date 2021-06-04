import pytest

from app import crud
from app.models import Post, User

"""
Fixtures for a random fake user
"""


@pytest.fixture
def fake_random_user_in_db(database, fake_schema_user_create) -> User:
    user = crud.user.create(fake_schema_user_create)
    yield user
    crud.user.remove(user.uid)


@pytest.fixture
def fake_link_post_in_db(
    database, fake_random_user_in_db, fake_schema_post_create_link
) -> Post:
    post = crud.post.create(fake_schema_post_create_link, fake_random_user_in_db)
    yield post
    crud.post.remove(post.uid)


@pytest.fixture
def fake_self_post_in_db(
    database, fake_random_user_in_db, fake_schema_post_create_self
) -> Post:
    post = crud.post.create(fake_schema_post_create_self, fake_random_user_in_db)
    yield post
    crud.post.remove(post.uid)


"""
Fixtures for the test user
"""


@pytest.fixture
def fake_test_user_in_db(fake_schema_test_user_create) -> User:
    user = crud.user.create(fake_schema_test_user_create)
    yield user
    crud.user.remove(user.uid)


@pytest.fixture
def fake_test_user_link_post_in_db(
    fake_test_user_in_db: User,
    fake_schema_post_create_link,
) -> Post:
    post = crud.post.create(fake_schema_post_create_link, fake_test_user_in_db)
    yield post
    crud.post.remove(post.uid)


"""
Fixtures for removing users and posts
"""


@pytest.fixture
def remove_user():
    def _remove(uid):
        crud.user.remove(uid)

    return _remove


@pytest.fixture
def remove_post():
    def _remove(uid):
        crud.post.remove(uid)

    return _remove

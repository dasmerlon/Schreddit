import pytest
from pydantic import UUID4

from app import crud
from app.models import (CommentContent, CommentMeta, PostContent, PostMeta,
                        Subreddit, User)
from app.tests.utils.fake_schemas import (CommentSchemas, PostSchemas,
                                          SubredditSchemas, UserSchemas)

"""
Fixtures for the test user
"""


@pytest.fixture
def test_user_in_db() -> User:
    user = crud.user.create(UserSchemas.get_create_test_user())
    yield user
    crud.user.remove(user.uid)


@pytest.fixture
def other_user_in_db() -> User:
    user = crud.user.create(UserSchemas.get_create_other_user())
    yield user
    crud.user.remove(user.uid)


@pytest.fixture
def post_link_in_db(
    test_user_in_db: User, subreddit_in_db: Subreddit
) -> (PostMeta, PostContent):
    schema = PostSchemas.get_create(type="link")
    post_meta = crud.post_meta.create(schema.metadata)
    post_content = crud.post_content.create(post_meta.uid, schema.content)
    crud.post_meta.set_author(post_meta, test_user_in_db)
    crud.post_meta.set_subreddit(post_meta, subreddit_in_db)
    yield post_meta, post_content
    crud.post_meta.remove(post_meta.uid)
    crud.post_content.remove(post_meta.uid)


@pytest.fixture
def post_self_in_db(
    test_user_in_db: User, subreddit_in_db: Subreddit
) -> (PostMeta, PostContent):
    schema = PostSchemas.get_create(type="self")
    post_meta = crud.post_meta.create(schema.metadata)
    post_content = crud.post_content.create(post_meta.uid, schema.content)
    crud.post_meta.set_author(post_meta, test_user_in_db)
    crud.post_meta.set_subreddit(post_meta, subreddit_in_db)
    yield post_meta, post_content
    crud.post_meta.remove(post_meta.uid)
    crud.post_content.remove(post_meta.uid)


@pytest.fixture
def post_self_in_db_upvoted(
    post_self_in_db_other_user: (PostMeta, PostContent), test_user_in_db: User
) -> (PostMeta, PostContent):
    post_meta = post_self_in_db_other_user[0]
    post_content = post_self_in_db_other_user[1]
    state = crud.post_meta.get_vote_state(post_meta, test_user_in_db)
    crud.post_meta.upvote(post_meta, test_user_in_db, state)
    yield post_meta, post_content
    crud.post_meta.remove(post_meta.uid)
    crud.post_content.remove(post_meta.uid)


@pytest.fixture
def post_self_in_db_other_user(
    other_user_in_db: User, subreddit_in_db: Subreddit
) -> (PostMeta, PostContent):
    schema = PostSchemas.get_create(type="self")
    post_meta = crud.post_meta.create(schema.metadata)
    post_content = crud.post_content.create(post_meta.uid, schema.content)
    crud.post_meta.set_author(post_meta, other_user_in_db)
    crud.post_meta.set_subreddit(post_meta, subreddit_in_db)
    yield post_meta, post_content
    crud.post_meta.remove(post_meta.uid)
    crud.post_content.remove(post_meta.uid)


@pytest.fixture
def comment_in_db(
    test_user_in_db: User, post_self_in_db: (PostMeta, PostContent)
) -> (CommentMeta, CommentContent):
    schema = CommentSchemas.get_create()
    comment_meta = crud.comment_meta.create(schema.metadata)
    comment_content = crud.comment_content.create(comment_meta.uid, schema.content)
    crud.comment_meta.set_author(comment_meta, test_user_in_db)
    crud.comment_meta.set_parent(comment_meta, post_self_in_db[0])
    yield comment_meta, comment_content
    crud.comment_meta.remove(comment_meta.uid)
    crud.comment_content.remove(comment_meta.uid)


@pytest.fixture
def comment_in_db_upvoted(
    comment_in_db: (CommentMeta, CommentContent), test_user_in_db: User
) -> (CommentMeta, CommentContent):
    comment_meta = comment_in_db[0]
    comment_content = comment_in_db[1]
    state = crud.comment_meta.get_vote_state(comment_meta, test_user_in_db)
    crud.comment_meta.upvote(comment_meta, test_user_in_db, state)
    yield comment_meta, comment_content
    crud.comment_meta.remove(comment_meta.uid)
    crud.comment_content.remove(comment_meta.uid)


@pytest.fixture
def comment_in_db_other_user(
    other_user_in_db: User, post_self_in_db: (PostMeta, PostContent)
) -> (CommentMeta, CommentContent):
    schema = CommentSchemas.get_create()
    comment_meta = crud.comment_meta.create(schema.metadata)
    comment_content = crud.comment_content.create(comment_meta.uid, schema.content)
    crud.comment_meta.set_author(comment_meta, other_user_in_db)
    crud.comment_meta.set_parent(comment_meta, post_self_in_db[0])
    yield comment_meta, comment_content
    crud.comment_meta.remove(comment_meta.uid)
    crud.comment_content.remove(comment_meta.uid)


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


@pytest.fixture
def remove_comments():
    """Add UUIDs of comments to this list that should be deleted after the test."""
    uids = []
    yield uids
    for uid in uids:
        if crud.comment_meta.get(UUID4(uid)) is not None:
            crud.comment_meta.remove(UUID4(uid))
        if crud.comment_content.get(UUID4(uid)) is not None:
            crud.comment_content.remove(UUID4(uid))

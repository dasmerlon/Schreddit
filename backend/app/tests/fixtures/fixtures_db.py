from datetime import datetime, timedelta, timezone
from typing import List, Tuple

import pytest
from pydantic import UUID4

from app import crud
from app.models import (CommentContent, CommentMeta, PostContent, PostMeta,
                        Subreddit, User)
from app.schemas import VoteOptions
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
def users_in_db() -> List[User]:
    user_list = []
    for i in range(5):
        user = crud.user.create(UserSchemas.get_create_enum_user(i))
        user_list.append(user)
    yield user_list
    for user in user_list:
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
def posts_with_votes_in_db(
    users_in_db: List[User],
    subreddits_in_db: List[Subreddit],
    test_user_in_db: User,
) -> List[Tuple[PostMeta, PostContent]]:
    post_list = []
    post_schemas = (
        PostSchemas.get_create(type="self"),
        PostSchemas.get_create(type="link"),
    )

    # create 5 posts in one subreddit by one author
    for i in range(5):
        post_meta = crud.post_meta.create(post_schemas[i % 2].metadata)
        post_content = crud.post_content.create(
            post_meta.uid, post_schemas[i % 2].content
        )
        crud.post_meta.set_author(post_meta, test_user_in_db)
        crud.post_meta.set_subreddit(post_meta, subreddits_in_db[0])
        # upvote the i-th post i times by the first i users in users_in_db
        for j in range(i):
            crud.post_meta.upvote(post_meta, users_in_db[j], VoteOptions.novote)
        # downvote the i-th post 5-i times by the last i users in users_in_db
        for j in range(i, 5):
            crud.post_meta.downvote(post_meta, users_in_db[j], VoteOptions.novote)
        post_list.insert(0, (post_meta, post_content))
    # make top post older to see difference between top and hot
    post_list[0][0].created_at = datetime.now(timezone.utc) - timedelta(days=1)
    post_list[0][0].save()

    # create 5 posts in the other subreddit authored by 5 different users
    other_post_list = []
    for i in range(5):
        post_meta = crud.post_meta.create(post_schemas[i % 2].metadata)
        post_content = crud.post_content.create(
            post_meta.uid, post_schemas[i % 2].content
        )
        crud.post_meta.set_author(post_meta, users_in_db[i])
        crud.post_meta.set_subreddit(post_meta, subreddits_in_db[1])
        other_post_list.append((post_meta, post_content))

    yield post_list

    # remove created posts
    for post_meta, post_content in post_list:
        crud.post_meta.remove(post_meta.uid)
        crud.post_content.remove(post_meta.uid)
    for post_meta, post_content in other_post_list:
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


@pytest.fixture
def subreddit_private_in_db(test_user_in_db: User) -> Subreddit:
    sr = crud.subreddit.create(SubredditSchemas.get_create(type="private"))
    crud.subreddit.set_admin(sr, test_user_in_db)
    yield sr
    crud.subreddit.remove(sr.uid)


@pytest.fixture
def subreddit_in_db_other_user(other_user_in_db: User) -> Subreddit:
    sr = crud.subreddit.create(SubredditSchemas.get_create(type="public"))
    crud.subreddit.set_admin(sr, other_user_in_db)
    yield sr
    crud.subreddit.remove(sr.uid)


@pytest.fixture
def subreddits_in_db(test_user_in_db: User) -> List[Subreddit]:
    subreddit_list = []
    for i in range(2):
        sr = crud.subreddit.create(
            SubredditSchemas.get_create_enum_sr(i, type="public")
        )
        crud.subreddit.set_admin(sr, test_user_in_db)
        subreddit_list.append(sr)
    yield subreddit_list
    for subreddit in subreddit_list:
        crud.subreddit.remove(subreddit.uid)


"""
Fixtures for removing users, posts, comments & subreddits
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


@pytest.fixture
def remove_subreddits():
    uids = []
    yield uids
    for uid in uids:
        if crud.subreddit.get(UUID4(uid)) is not None:
            crud.subreddit.remove(UUID4(uid))
        if crud.subreddit.get(UUID4(uid)) is not None:
            crud.subreddit.remove(UUID4(uid))
        if crud.comment_meta.get(uid) is not None:
            crud.comment_meta.remove(uid)
        if crud.comment_content.get(uid) is not None:
            crud.comment_content.remove(uid)
        if crud.comment_meta.get(UUID4(uid)) is not None:
            crud.comment_meta.remove(UUID4(uid))
        if crud.comment_content.get(UUID4(uid)) is not None:
            crud.comment_content.remove(UUID4(uid))

from typing import List, Tuple
from uuid import uuid4

import pytest

from app import crud
from app.models import PostContent, PostMeta, Subreddit, User
from app.schemas import CursorDirection, PostSort
from app.tests.utils.fake_schemas import PostSchemas


def test_get_post_by_uid(post_self_in_db: (PostMeta, PostContent)) -> None:
    metadata = post_self_in_db[0]
    content = post_self_in_db[1]
    post_meta = crud.post_meta.get(metadata.uid)
    post_content = crud.post_content.get(metadata.uid)
    assert post_meta
    assert post_meta == metadata
    assert post_content
    assert post_content == content


def test_get_post_by_uid_fail() -> None:
    post_meta = crud.post_meta.get(uuid4())
    post_content = crud.post_content.get(uuid4())
    assert post_meta is None
    assert post_content is None


@pytest.mark.parametrize(
    "sort",
    [PostSort.new, PostSort.top, PostSort.hot],
)
@pytest.mark.parametrize("user_auth", [True, False])
def test_get_posts(
    posts_with_votes_in_db: List[Tuple[PostMeta, PostContent]],
    subreddits_in_db: Subreddit,
    users_in_db: List[User],
    sort: PostSort,
    user_auth: bool,
) -> None:
    def sort_post_list(post_list: List[Tuple[PostMeta, PostContent]], order: PostSort):
        if order == PostSort.new:
            post_list.append(post_list.pop(0))
        elif order == PostSort.top:
            pass
        elif order == PostSort.hot:
            post_list.insert(4, post_list.pop(0))
        return post_list

    # pick logged in user to get vote state for
    if user_auth:
        user = users_in_db[0]
    else:
        user = None

    # set subreddit to get posts from
    subreddit = subreddits_in_db[0]

    # copy list of posts and order correctly according to `sort`
    sorted_list = sort_post_list(posts_with_votes_in_db.copy(), sort)

    # test sorting order
    posts = crud.post_meta.get_posts(subreddit, user, None, None, sort, 25)

    for i in range(len(posts) - 1):
        assert posts[i]["uid"] == sorted_list[i][0].uid

    # test vote state
    for i in range(len(posts)):
        if user_auth:
            post = crud.post_meta.get(posts[i]["uid"])
            assert posts[i]["state"] == crud.thing_meta.get_vote_state(post, user)
        else:
            assert posts[i]["state"] == 0

    # test cursors
    posts = crud.post_meta.get_posts(
        subreddit, user, sorted_list[1][0], CursorDirection.after, sort, 3
    )
    for i in range(3):
        assert posts[i]["uid"] == sorted_list[2 + i][0].uid
    posts = crud.post_meta.get_posts(
        subreddit, user, sorted_list[4][0], CursorDirection.before, sort, 3
    )
    print([meta.uid for meta, content in sorted_list])
    print([post["uid"] for post in posts])
    for i in range(3):
        assert posts[i]["uid"] == sorted_list[1 + i][0].uid


def test_create_post(
    test_user_in_db: User, subreddit_in_db: Subreddit, remove_posts: List
) -> None:
    obj_in = PostSchemas.get_create(type="link")
    obj_in.metadata.sr = subreddit_in_db.sr
    post_metadata = crud.post_meta.create(obj_in.metadata)
    post_content = crud.post_content.create(post_metadata.uid, obj_in.content)
    crud.post_meta.set_author(post_metadata, test_user_in_db)
    crud.post_meta.set_subreddit(post_metadata, subreddit_in_db)
    author = post_metadata.author.single()
    subreddit = post_metadata.subreddit.single()
    remove_posts.append(post_metadata.uid)
    for key in obj_in.metadata.dict():
        if key != "sr":
            assert getattr(obj_in.metadata, key) == getattr(post_metadata, key)
    for key in obj_in.content.dict():
        assert getattr(obj_in.content, key) == getattr(post_content, key)
    assert author.email == test_user_in_db.email
    assert author.username == test_user_in_db.username
    assert obj_in.metadata.sr == subreddit.sr


def test_update_post(post_link_in_db: (PostMeta, PostContent)) -> None:
    metadata = post_link_in_db[0]
    content = post_link_in_db[1]
    obj_in = PostSchemas.get_update(type="link")
    crud.post_meta.update(metadata, obj_in.metadata)
    crud.post_content.update(content, obj_in.content)
    updated_post_metadata = crud.post_meta.get(metadata.uid)
    updated_post_content = crud.post_content.get(metadata.uid)
    assert updated_post_metadata.uid == metadata.uid
    for key in obj_in.metadata.dict():
        assert getattr(updated_post_metadata, key) == getattr(obj_in.metadata, key)
    for key in obj_in.content.dict():
        assert getattr(updated_post_content, key) == getattr(obj_in.content, key)

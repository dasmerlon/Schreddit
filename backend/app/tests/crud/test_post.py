from typing import List
from uuid import uuid4

from app import crud
from app.models import Post, User
from app.tests.utils.fake_schemas import PostSchemas


def test_get_post_by_uid(post_self_in_db: Post) -> None:
    post = crud.post.get(post_self_in_db.uid)
    assert post
    assert post == post_self_in_db


def test_get_post_by_uid_fail() -> None:
    post = crud.post.get(uuid4())
    assert post is None


def test_create_post(test_user_in_db: User, remove_posts: List) -> None:
    obj_in = PostSchemas.get_create(type="link")
    post = crud.post.create(obj_in, test_user_in_db)
    author = post.author.single()
    remove_posts.append(post.uid)
    for key in obj_in.dict():
        if key != "sr":
            assert getattr(obj_in, key) == getattr(post, key)
    assert author.email == test_user_in_db.email
    assert author.username == test_user_in_db.username
    # TODO: assert subreddit


def test_update_post(post_link_in_db: Post) -> None:
    obj_in = PostSchemas.get_update(type="link")
    updated_post = crud.post.update(post_link_in_db, obj_in)
    assert updated_post.uid == post_link_in_db.uid
    for key in obj_in.dict():
        assert getattr(updated_post, key) == getattr(obj_in, key)

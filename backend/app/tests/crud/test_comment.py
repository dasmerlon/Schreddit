from typing import List
from uuid import uuid4

from app import crud
from app.models import CommentContent, CommentMeta, PostContent, PostMeta, User
from app.tests.utils.fake_schemas import CommentSchemas


def test_get_comment_by_uid(comment_in_db: (CommentMeta, CommentContent)) -> None:
    metadata = comment_in_db[0]
    content = comment_in_db[1]
    comment_meta = crud.comment_meta.get(metadata.uid)
    comment_content = crud.comment_content.get(metadata.uid)
    assert comment_meta
    assert comment_meta == metadata
    assert comment_content
    assert comment_content == content


def test_get_comment_by_uid_fail() -> None:
    comment_meta = crud.comment_meta.get(uuid4())
    comment_content = crud.comment_content.get(uuid4())
    assert comment_meta is None
    assert comment_content is None


def test_create_comment(
    test_user_in_db: User,
    post_self_in_db: (PostMeta, PostContent),
    remove_comments: List,
) -> None:
    obj_in = CommentSchemas.get_create()
    comment_metadata = crud.comment_meta.create(obj_in.metadata)
    comment_content = crud.comment_content.create(comment_metadata.uid, obj_in.content)
    crud.comment_meta.set_author(comment_metadata, test_user_in_db)
    crud.comment_meta.set_parent(comment_metadata, post_self_in_db[0])
    author = comment_metadata.author.single()
    parent = comment_metadata.parent.single()
    remove_comments.append(comment_metadata.uid)
    assert obj_in.content.text == comment_content.text
    assert author == test_user_in_db
    assert post_self_in_db[0].uid == parent.uid


def test_update_comment(comment_in_db: (CommentMeta, CommentContent)) -> None:
    metadata = comment_in_db[0]
    content = comment_in_db[1]
    obj_in = CommentSchemas.get_update()
    crud.comment_meta.update(metadata, obj_in.metadata)
    crud.comment_content.update(content, obj_in.content)
    updated_comment_metadata = crud.comment_meta.get(metadata.uid)
    updated_comment_content = crud.comment_content.get(metadata.uid)
    assert updated_comment_metadata.uid == metadata.uid
    assert updated_comment_content.text == obj_in.content.text

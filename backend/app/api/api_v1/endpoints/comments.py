from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (CommentNotFoundException,
                                       ParentNotFoundException,
                                       UnauthorizedUpdateException)

router = APIRouter()


@router.get(
    "/{uid}",
    name="Get a comment",
    response_model=schemas.Comment,
    status_code=status.HTTP_200_OK,
)
def get_comment(uid: UUID4):
    """
    Return a comment.

    - `uid`: UUID of the comment to return
    """
    comment_meta = crud.comment_meta.get(uid)
    comment_content = crud.comment_content.get(uid)
    if not comment_meta or not comment_content:
        raise CommentNotFoundException

    return schemas.Comment(metadata=comment_meta, content=comment_content)


@router.post(
    "/{parent}",
    name="Submit a comment",
    response_model=schemas.Comment,
    status_code=status.HTTP_201_CREATED,
)
def submit_comment(
    parent: UUID4,
    comment: schemas.CommentCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Submit a comment to a `parent` thing.

    - `parent`: UUID of a thing; parent of the new comment
    - `text`: content of the comment
    """
    parent_thing = crud.thing_meta.get(parent)
    if not parent_thing:
        raise ParentNotFoundException

    # create comment
    metadata = crud.comment_meta.create(comment.metadata)
    content = crud.comment_content.create(metadata.uid, comment.content)
    crud.comment_meta.set_author(metadata, current_user)
    crud.comment_meta.set_parent(metadata, parent_thing)

    return schemas.Comment(metadata=metadata, content=content)


@router.put(
    "/{uid}",
    name="Update a comment",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_comment(
    uid: UUID4,
    comment: schemas.CommentUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a comment.

    - `uid`: UUID of the comment to update
    - `text`: content of the comment
    """
    old_comment_meta = crud.comment_meta.get(uid)
    old_comment_content = crud.comment_content.get(uid)
    if not old_comment_meta or not old_comment_content:
        raise CommentNotFoundException
    if crud.comment_meta.get_author(old_comment_meta) != current_user:
        raise UnauthorizedUpdateException

    crud.comment_meta.update(old_comment_meta, None)
    crud.comment_content.update(old_comment_content, comment.content)

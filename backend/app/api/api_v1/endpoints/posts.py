from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (PaginationAfterAndBeforeException,
                                       PaginationInvalidCursorException,
                                       PostNotFoundException,
                                       PostTypeRequestInvalidException,
                                       SubredditNotFoundException)

router = APIRouter()


@router.get(
    "",
    name="Get Posts",
    response_model=schemas.PostList,
    status_code=status.HTTP_200_OK,
)
def get_posts(
    request: Request,
    after: Optional[UUID4] = None,
    before: Optional[UUID4] = None,
    sort: Optional[schemas.PostSort] = schemas.PostSort.new,
    size: Optional[int] = Query(25, gt=0, le=100),
):
    # act depending on which cursor is passed
    if after and before:
        raise PaginationAfterAndBeforeException
    elif not after and not before:
        results = crud.post.get_posts_after(None, sort, size)
    elif after:
        cursor = crud.post.get(after)
        if cursor is None:
            raise PaginationInvalidCursorException
        results = crud.post.get_posts_after(cursor, sort, size)
    elif before:
        cursor = crud.post.get(before)
        if cursor is None:
            raise PaginationInvalidCursorException
        results = crud.post.get_posts_before(cursor, sort, size)

    basepath = f"{request.url.path}?sort={sort}"
    next = f"{basepath}&after={results[-1].uid}" if results else None
    prev = f"{basepath}&before={results[0].uid}" if results else None

    # set pagination
    links = schemas.Pagination(next=next, prev=prev)
    return schemas.PostList(links=links, data=results)


@router.get(
    "/{post_uid}",
    name="Get Post",
    response_model=schemas.Post,
    status_code=status.HTTP_200_OK,
)
def get_post(post_uid: UUID4):
    post = crud.post.get(post_uid)
    if post is None:
        raise PostNotFoundException
    return post


@router.post(
    "",
    name="Submit Post",
    response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED,
)
def submit_post(
    post: schemas.PostCreate, current_user: models.User = Depends(deps.get_current_user)
):
    """
    Submit a post to the subreddit `sr` with the title `title`.
    If `type` is `"link"`, then `url` is expected to be a valid URL to link to.
    Otherwise, `text` will be the body of the self-post.

    - `nsfw` : `boolean` value
    - `spoiler` : `boolean` value
    - `sr` : subreddit name
    - `text` : raw markdown text
    - `title` : title of the submission, up to 300 characters long
    - `type` : one of `link`, `self`, `image`, `video`, `videogif`)
    - `url` : a valid URL
    """
    if post.type == schemas.PostType.link and (not post.url or post.text):
        raise PostTypeRequestInvalidException
    elif post.type != schemas.PostType.link and (not post.text or post.url):
        raise PostTypeRequestInvalidException

    # check if subreddit exists
    sr = crud.subreddit.get_by_sr(post.sr)
    if sr is None:
        raise SubredditNotFoundException

    # create post
    created_post = crud.post.create(post)
    crud.post.set_author(created_post, current_user)
    crud.post.set_subreddit(created_post, sr)

    return created_post


@router.put(
    "/{post_uid}",
    name="Edit Post",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_post(
    post_uid: UUID4,
    post: schemas.PostUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a post.

    - `nsfw` : `boolean` value
    - `spoiler` : `boolean` value
    - `text` : raw markdown text
    - `title` : title of the submission, up to 300 characters long
    - `uid` : the unique ID of the post to be updated
    - `url` : a valid URL
    """
    old_post = crud.post.get(post_uid)
    if old_post is None:
        raise PostNotFoundException
    if old_post.type == schemas.PostType.link.value and post.text is not None:
        raise PostTypeRequestInvalidException
    elif old_post.type != schemas.PostType.link.value and post.url is not None:
        raise PostTypeRequestInvalidException
    crud.post.update(old_post, post)

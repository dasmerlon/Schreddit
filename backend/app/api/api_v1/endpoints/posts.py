from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (PaginationAfterAndBeforeException,
                                       PaginationInvalidCursorException,
                                       PostNotFoundException,
                                       PostTypeRequestInvalidException,
                                       SubredditNotFoundException,
                                       UnauthorizedUpdateException)

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
    """
    Return a range of up to `limit` posts with an optional sorting order.
    If `sort` is not passed, posts are returned in descending order of their creation.

    `after` and `before` are cursors for pagination and refer to a post. Only one cursor
    should be specified.

    - `after` : get posts including and after this cursor
    - `before` : get posts including and before this cursor
    - `sort` : sorting order, one of `best`, `hot`, `new`, `top`
    - `limit` : maximum number of posts to return
    """
    # act depending on which cursor is passed
    if after and before:
        raise PaginationAfterAndBeforeException
    elif not after and not before:
        results = crud.post_meta.get_posts_after(None, sort, size)
    elif after:
        cursor = crud.post_meta.get(after)
        if cursor is None:
            raise PaginationInvalidCursorException
        results = crud.post_meta.get_posts_after(cursor, sort, size)
    elif before:
        cursor = crud.post_meta.get(before)
        if cursor is None:
            raise PaginationInvalidCursorException
        results = crud.post_meta.get_posts_before(cursor, sort, size)

    basepath = f"{request.url.path}?sort={sort}"
    next = f"{basepath}&after={results[-1].uid}" if results else None
    prev = f"{basepath}&before={results[0].uid}" if results else None

    # retrieve post content
    contents = crud.post_content.filter_by_uids([r.uid for r in results])

    # set pagination
    links = schemas.Pagination(next=next, prev=prev)
    return schemas.PostList(
        links=links,
        data=[
            schemas.Post(metadata=r, content=contents.get(uid=r.uid)) for r in results
        ],
    )


@router.get(
    "/{uid}",
    name="Get Post",
    response_model=schemas.Post,
    status_code=status.HTTP_200_OK,
)
def get_post(uid: UUID4):
    """
    Return a post by its UUID.

    - `uid` : the UUID of the post to return
    """
    post_meta = crud.post_meta.get(uid)
    post_content = crud.post_content.get(uid)
    if not post_meta or not post_content:
        raise PostNotFoundException

    return schemas.Post(metadata=post_meta, content=post_content)


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
    # check if subreddit exists
    sr = crud.subreddit.get_by_sr(post.metadata.sr)
    if sr is None:
        raise SubredditNotFoundException

    # create post
    created_post_meta = crud.post_meta.create(post.metadata)
    created_post_content = crud.post_content.create(created_post_meta.uid, post.content)
    crud.post_meta.set_author(created_post_meta, current_user)
    crud.post_meta.set_subreddit(created_post_meta, sr)

    return schemas.Post(metadata=created_post_meta, content=created_post_content)


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
    old_post_meta = crud.post_meta.get(post_uid)
    old_post_content = crud.post_content.get(post_uid)
    if not old_post_meta or not old_post_content:
        raise PostNotFoundException
    if crud.post_meta.get_author(old_post_meta) != current_user:
        raise UnauthorizedUpdateException
    if old_post_meta.type == schemas.PostType.link.value and (
            post.content.text is not None or post.content.url is None
    ):
        raise PostTypeRequestInvalidException
    elif old_post_meta.type != schemas.PostType.link.value and (
            post.content.text is None or post.content.url is not None
    ):
        raise PostTypeRequestInvalidException

    crud.post_meta.update(old_post_meta, post.metadata)
    crud.post_content.update(old_post_content, post.content)

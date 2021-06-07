from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import UUID4

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "",
    name="Get Posts",
    response_model=schemas.PostList,
    status_code=status.HTTP_200_OK,
)
def get_posts(
    after: Optional[UUID4] = None,
    before: Optional[UUID4] = None,
    sort: Optional[schemas.PostSort] = schemas.PostSort.new,
    limit: Optional[int] = Query(25, gt=0, le=100),
):
    if after is not None and before is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The parameters 'after' and 'before' should not be specified both.",
        )
    if (after is not None and crud.post.get(after.hex) is None) or (
        before is not None and crud.post.get(before.hex) is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The cursor does not reference an existing post.",
        )
    results = crud.post.get_selection(after, before, sort, limit)
    new_after, new_before = crud.post.get_new_cursors(results, sort)
    # set pagination
    pagination = schemas.Pagination(after=new_after, before=new_before, limit=limit)
    return schemas.PostList(pagination=pagination, results=results)


@router.get(
    "/{post_uid}",
    name="Get Post",
    response_model=schemas.Post,
    status_code=status.HTTP_200_OK,
)
def get_post(post_uid: UUID4):
    post = crud.post.get(post_uid)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The post was not found."
        )
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
    if post.type == schemas.PostType.link and (
        post.url is None or post.text is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posts of type 'link' must include a 'url' parameter"
            "and must not include a 'text' parameter.",
        )
    elif post.type != schemas.PostType.link and (not post.text or post.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posts of type other than 'link' must include a 'text' parameter"
            "and must not include a 'url' parameter.",
        )
    # TODO: throw exception if subreddit does not exist
    created_post = crud.post.create(post, current_user)
    # TODO: uncomment when subreddit logic is implemented
    # subreddit = crud.post.set_subreddit(created_post, subreddit)
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The post you want to update does not exist.",
        )
    if old_post.type == schemas.PostType.link.value and post.text is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posts of type 'link' must include a 'url' parameter"
            "and must not include a 'text' parameter.",
        )
    elif old_post.type != schemas.PostType.link.value and post.url is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posts of type other than 'link' must include a 'text' parameter"
            "and must not include a 'url' parameter.",
        )
    crud.post.update(old_post, post)

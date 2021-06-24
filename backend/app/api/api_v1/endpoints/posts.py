from fastapi import APIRouter, Depends, HTTPException, status

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


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
            detail="Posts of type 'link' must include a 'url' parameter and must not include a 'text' parameter.",
        )
    elif post.type != schemas.PostType.link and (not post.text or post.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posts of type other than 'link' must include a 'text' parameter and must not include a 'url' parameter.",
        )
    # TODO: throw exception if subreddit does not exist
    created_post = crud.post.create(post)
    author = crud.post.set_author(created_post, current_user)
    # TODO: uncomment when subreddit logic is implemented
    # subreddit = crud.post.set_subreddit(db_obj=created_post, subreddit=subreddit)
    post_out = schemas.Post.from_orm(created_post)
    post_out.author = author
    return post_out
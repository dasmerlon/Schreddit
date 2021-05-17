from fastapi import APIRouter
from app import crud, models, schemas

router = APIRouter()


@router.post("/submit", name="Submit Post", response_model=schemas.Post)
async def submit_post(post: schemas.PostCreate):
    """
    Submit a post to the subreddit `sr` with the title `title`.
    If `kind` is `"link"`, then `url` is expected to be a valid URL to link to.
    Otherwise, `text` will be the body of the self-post.

    - `nsfw` : `boolean` value
    - `spoiler` : `boolean` value
    - `sr` : subreddit name
    - `text` : raw markdown text
    - `title` : title of the submission, up to 300 characters long
    - `type` : one of `link`, `self`, `image`, `video`, `videogif`)
    - `url` : a valid URL
    """
    # get user identity from JWT auth token
    crud.post.create(post)
    return post

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import SubredditNotFoundException

router = APIRouter()


@router.post(
    "/r/{sr}",
    name="Create Subreddit",
    response_model=schemas.Subreddit,
    status_code=status.HTTP_201_CREATED,
)
def create_subreddit(
    subreddit: schemas.SubredditCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create a new Subreddit `sr` with the title `title`.

    - `description` : raw text
    - `sr` : unique subreddit name
    - `title` : title of the subreddit, up to 100 characters long
    - `type` : one of `archived`, `private`, `public`, `restricted`, `user`
    """
    if crud.subreddit.get_by_sr(subreddit.sr) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A subreddit with this name already exists.",
        )
    created_subreddit = crud.subreddit.create(subreddit)
    crud.subreddit.set_admin(created_subreddit, current_user)

    return created_subreddit


@router.get(
    "/{sr}",
    name="Get Subreddit",
    response_model=schemas.Subreddit,
    status_code=status.HTTP_200_OK,
)
def get_subreddit(subreddit: str):
    """
    Get Subreddit by sr
    """
    sr = crud.subreddit.get_by_sr(subreddit)
    if sr is None:
        raise SubredditNotFoundException
    return sr


@router.put(
    "/{sr}",
    name="Edit Subreddit",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_subreddit(
    sr: str,
    subreddit: schemas.SubredditUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a Subreddit.

    - `description` : raw markdown text
    - `title` : title of the subreddit, up to 300 characters long
    - `type` : subreddit type
    """
    old_sr = crud.subreddit.get_by_sr(sr)
    if old_sr is None:
        raise SubredditNotFoundException
    crud.subreddit.update(old_sr, subreddit)

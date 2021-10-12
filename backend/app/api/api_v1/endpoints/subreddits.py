from fastapi import APIRouter, Depends, Response, status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (SubredditAlreadyExistsException,
                                       SubredditNotFoundException,
                                       UnauthorizedUpdateException)

router = APIRouter()


@router.post(
    "",
    name="Create a subreddit",
    response_model=schemas.Subreddit,
    status_code=status.HTTP_201_CREATED,
)
def create_subreddit(
    subreddit: schemas.SubredditCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create a new subreddit.

    - `description`: description of the subreddit
    - `sr`: unique subreddit name, between 3 and 21 characters long
    - `title`: title of the subreddit
    - `type`: one of `archived`, `private`, `public`, `restricted`, `user`
    """
    if crud.subreddit.get_by_sr(subreddit.sr) is not None:
        raise SubredditAlreadyExistsException
    created_subreddit = crud.subreddit.create(subreddit)
    crud.subreddit.set_admin(created_subreddit, current_user)

    return created_subreddit


@router.get(
    "/{sr}",
    name="Get a subreddit",
    response_model=schemas.Subreddit,
    status_code=status.HTTP_200_OK,
)
def get_subreddit(sr: str):
    """
    Return a subreddit.

    - `sr`: name of the subreddit
    """
    get_sr = crud.subreddit.get_by_sr(sr)
    if not get_sr:
        raise SubredditNotFoundException
    return get_sr


@router.put(
    "/{sr}",
    name="Update a subreddit",
    response_class=Response,
)
def update_subreddit(
    sr: str,
    sr_update: schemas.SubredditUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a subreddit.

    - `sr`: name of the subreddit to edit
    - `description`: description of the subreddit
    - `title`: title of the subreddit
    """
    to_update = {}  # collect all changes made
    old_sr = crud.subreddit.get_by_sr(sr)

    if old_sr is None:
        raise SubredditNotFoundException
    if crud.subreddit.get_admin(old_sr) != current_user:
        raise UnauthorizedUpdateException
    if old_sr.description != sr_update.description:
        to_update["description"] = sr_update.description
    if old_sr.title != sr_update.title:
        to_update["title"] = sr_update.title
    if not to_update:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    crud.subreddit.update(old_sr, sr_update)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

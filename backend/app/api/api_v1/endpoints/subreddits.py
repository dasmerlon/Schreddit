from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (SubredditNotFoundException,
                                       UnauthorizedUpdateException)

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
    "/r/{sr}",
    name="Get Subreddit",
    response_model=schemas.Subreddit,
    status_code=status.HTTP_200_OK,
)
def get_subreddit(sr: str):
    """
    Get Subreddit by sr

    - `str` : the name of the subreddit
    """
    get_sr = crud.subreddit.get_by_sr(sr)
    if not get_sr:
        raise SubredditNotFoundException
    return get_sr


@router.get(
    "/search",
    name="Search Subreddit",
    response_model=List[schemas.Subreddit],
    status_code=status.HTTP_200_OK,
)
def search_subreddit(q: str, include_title: Optional[bool] = False):
    """
    Search a subreddit and return a list of matching subreddits

    :param q: a search_string
    :param include_title: ``True`` if the subreddit titles should also be searched
    """
    sr_list = crud.subreddit.search(q, include_title)
    print(sr_list)
    return sr_list


@router.put(
    "/r/{sr}",
    name="Edit Subreddit",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_subreddit(
    sr: str,
    sr_update: schemas.SubredditUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a Subreddit.

    - `description` : raw markdown text
    - `title` : title of the subreddit, up to 300 characters long
    - `type` : subreddit type
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
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="No changes have been made.",
        )
    crud.subreddit.update(old_sr, sr_update)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

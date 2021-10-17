from typing import List, Optional

from fastapi import APIRouter, status

from app import crud, schemas

router = APIRouter()


@router.get(
    "",
    name="Search for a subreddit",
    response_model=List[schemas.Subreddit],
    status_code=status.HTTP_200_OK,
)
def search_subreddit(q: str, include_title: Optional[bool] = False):
    """
    Search for a subreddit and return a list of matching subreddits.

    - `q`: a search string
    - `include_title`: `True` if subreddit titles should be included in the search
    """
    sr_list = crud.subreddit.search(q, include_title)
    return sr_list

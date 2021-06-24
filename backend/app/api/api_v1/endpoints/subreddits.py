from fastapi import APIRouter, Depends, HTTPException, status

from app import crud, models, schemas
from app.api import deps

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

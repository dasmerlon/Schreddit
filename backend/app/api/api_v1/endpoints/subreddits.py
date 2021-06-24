from fastapi import APIRouter, Depends, status

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
    created_subreddit = crud.subreddit.create(obj_in=subreddit)
    admin = crud.subreddit.set_admin(db_obj=created_subreddit, admin=current_user)

    subreddit_out = schemas.Subreddit.from_orm(created_subreddit)
    subreddit_out.admin = admin

    return subreddit_out

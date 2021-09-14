from fastapi import APIRouter, Depends, Response, status

from app import crud, models
from app.api import deps
from app.api.api_v1.exceptions import SubredditNotFoundException

router = APIRouter()


@router.post(
    "/subscribe",
    name="Subscribe to subreddit",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def subscribe(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    # check if subreddit exists
    subreddit = crud.subreddit.get_by_sr(sr)
    if subreddit is None:
        raise SubredditNotFoundException

    # check if subreddit is already subscribed
    #TODO

    # create subscription
    crud.user.set_subscription(current_user, subreddit)


@router.delete(
    "/unsubscribe",
    name="Unsubscribe to subreddit",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def unsubscribe(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    # check if subreddit exists
    subreddit = crud.subreddit.get_by_sr(sr)
    if subreddit is None:
        raise SubredditNotFoundException

    # check if subreddit is already unsubscribed
    # TODO

    # delete subscription
    crud.user.delete_subscription(current_user, subreddit)

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
    # TODO

    # create subscription
    crud.subreddit.set_subscription(subreddit, current_user)


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
    crud.subreddit.end_subscription(subreddit, current_user)


@router.get(
    "/{sr}/subscriber",
    name="Get subscriber count of a subreddit",
    status_code=status.HTTP_200_OK,
)
def get_subscriber_count(sr: str):
    subreddit = crud.subreddit.get_by_sr(sr)
    if subreddit is None:
        raise SubredditNotFoundException

    return crud.subreddit.get_subscriber_count(subreddit)

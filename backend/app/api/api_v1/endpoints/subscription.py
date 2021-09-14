from fastapi import APIRouter, Depends, Response, status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (SubredditAlreadySubscribed,
                                       SubredditNotFoundException,
                                       SubredditNotSubscribed)

router = APIRouter()


@router.post(
    "/subscribe/{sr}",
    name="Subscribe to subreddit",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def subscribe(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    subreddit = crud.subreddit.get_by_sr(sr)

    # check if subreddit exists
    if subreddit is None:
        raise SubredditNotFoundException

    state = crud.subreddit.get_subscription_status(subreddit, current_user)

    # check if subreddit is already subscribed TODO
    if state == schemas.SubscriptionStatus.subscribed:
        raise SubredditAlreadySubscribed

    # create subscription
    elif state == schemas.SubscriptionStatus.unsubscribed:
        crud.subreddit.set_subscription(subreddit, current_user)


@router.delete(
    "/unsubscribe/{sr}",
    name="Unsubscribe to subreddit",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def unsubscribe(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    subreddit = crud.subreddit.get_by_sr(sr)

    # check if subreddit exists
    if subreddit is None:
        raise SubredditNotFoundException

    state = crud.subreddit.get_subscription_status(subreddit, current_user)

    # check if subreddit is already subscribed TODO
    if state == schemas.SubscriptionStatus.unsubscribed:
        raise SubredditNotSubscribed

    # end subscription
    elif state == schemas.SubscriptionStatus.subscribed:
        crud.subreddit.end_subscription(subreddit, current_user)


@router.get(
    "/{sr}/state",
    name="Get subscription state of a subreddit",
    response_model=schemas.SubscriptionStatus,
    status_code=status.HTTP_200_OK,
)
def get_subscription_status(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    subreddit = crud.subreddit.get_by_sr(sr)

    # check if subreddit exists
    if subreddit is None:
        raise SubredditNotFoundException

    return crud.subreddit.get_subscription_status(subreddit, current_user)


@router.get(
    "/{sr}/subscriber",
    name="Get subscriber count of a subreddit",
    status_code=status.HTTP_200_OK,
)
def get_subscriber_count(sr: str):
    subreddit = crud.subreddit.get_by_sr(sr)

    # check if subreddit exists
    if subreddit is None:
        raise SubredditNotFoundException

    return crud.subreddit.get_subscriber_count(subreddit)

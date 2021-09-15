from fastapi import APIRouter, Depends, Response, status

from app import crud, models
from app.api import deps
from app.api.api_v1.exceptions import SubredditNotFoundException

router = APIRouter()


@router.put(
    "/{sr}/sub",
    name="Subscribe to subreddit",
)
def subscribe(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    subreddit = crud.subreddit.get_by_sr(sr)

    # check if subreddit exists
    if subreddit is None:
        raise SubredditNotFoundException

    subscribed = crud.subreddit.is_subscribed(subreddit, current_user)

    # check if subreddit is already subscribed
    if subscribed:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    # create subscription
    elif not subscribed:
        crud.subreddit.set_subscription(subreddit, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{sr}/unsub",
    name="Unsubscribe to subreddit",
)
def unsubscribe(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    subreddit = crud.subreddit.get_by_sr(sr)

    # check if subreddit exists
    if subreddit is None:
        raise SubredditNotFoundException

    subscribed = crud.subreddit.is_subscribed(subreddit, current_user)

    # check if subreddit is already subscribed
    if not subscribed:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    # end subscription
    elif subscribed:
        crud.subreddit.end_subscription(subreddit, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{sr}/state",
    name="Get subscription state of a subreddit",
    status_code=status.HTTP_200_OK,
)
def is_subscribed(
    sr: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    subreddit = crud.subreddit.get_by_sr(sr)

    # check if subreddit exists
    if subreddit is None:
        raise SubredditNotFoundException

    return crud.subreddit.is_subscribed(subreddit, current_user)


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

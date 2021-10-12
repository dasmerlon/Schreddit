import re
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (UserAlreadyExistsException,
                                       UserNotFoundException)
from app.core.security import verify_password

router = APIRouter()


@router.post(
    "",
    name="Register a user",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserCreate):
    """
    Register a new user.

    - `email`: valid email address
    - `username`: unique username
    - `password`: password
    """
    username_exists = crud.user.get_by_username(user.username)
    if username_exists:
        raise UserAlreadyExistsException
    email_exists = crud.user.get_by_email(user.email)
    if email_exists:
        raise UserAlreadyExistsException
    registered_user = crud.user.create(user)
    return registered_user


@router.get(
    "/u/{username}",
    name="Get a user's data",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
def get_user(username: str):
    """
    Get the user data from an existing user.

    - `username`: username or email of the user to return
    """
    # check if `username` is valid email
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", username):
        user = crud.user.get_by_email(username)
        if user is None:
            user = crud.user.get_by_username(username)
    else:
        user = crud.user.get_by_username(username)
    if user is None:
        raise UserNotFoundException
    return user


@router.put(
    "",
    name="Update user data",
)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update the data of the logged in user.

    - `email`: new email address
    - `password`: new password
    """
    to_update = {}

    # Check if we got a new and different email.
    if user_update.email is not None and user_update.email != current_user.email:
        to_update["email"] = user_update.email

    # Check if the password changed.
    if user_update.password and not verify_password(
        user_update.password, current_user.hashed_password
    ):
        to_update["password"] = user_update.password

    if not bool(to_update):
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    crud.user.update(current_user, to_update)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/subscriptions",
    name="Get subscribed subreddits",
    response_model=schemas.SubredditList,
    status_code=status.HTTP_200_OK,
)
def get_subscriptions(
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Return all subreddits that the logged in user has subscribed in alphabetical order.
    """
    return schemas.SubredditList(subreddits=crud.user.get_subscriptions(current_user))


@router.get(
    "/recommendations",
    name="Get recommended subreddits",
    response_model=schemas.SubredditList,
    status_code=status.HTTP_200_OK,
)
def get_recommendations(
    limit: Optional[int] = Query(5, gt=0, le=100),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Return recommended subreddits for the logged in user, sorted by a score of
    relevance.

    - `limit`: maximum number of recommendations to return
    """
    sr_list = crud.user.get_recommendations(current_user, limit)
    return schemas.SubredditList(subreddits=sr_list)

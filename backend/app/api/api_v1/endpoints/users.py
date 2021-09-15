from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import DeflateError

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import UserNotFoundException
from app.core.security import verify_password

router = APIRouter()


@router.post(
    "/register",
    name="Register User",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserCreate):
    """
    Register a new user with a valid `email` address, a `username` and a `password`.
    """
    username_exists = crud.user.get_by_username(user.username)
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this username already exists.",
        )
    email_exists = crud.user.get_by_email(user.email)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this e-mail address already exists.",
        )
    registered_user = crud.user.create(user)
    return registered_user


@router.get(
    "/{username}",
    name="Get User Data",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
def get_user(username: str):
    """
    Get user data from an existing user via email or username.
    If everything succeeds, a user with matching email or username will be returned.
    """
    try:
        user = crud.user.get_by_email(username)
    except:
        user = crud.user.get_by_username(username)
    if user is None:
        raise UserNotFoundException
    return user


@router.put(
    "/settings",
    name="Update User Data",
)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a user's data.
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

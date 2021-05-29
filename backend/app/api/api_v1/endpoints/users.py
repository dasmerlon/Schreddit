from fastapi import APIRouter, Depends, HTTPException, status

from app import crud, models, schemas
from app.api import deps

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
    Get user data from an existing user.
    """
    user = crud.user.get_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists.",
        )
    return user


@router.put(
    "/settings",
    name="Update User Data",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a user's data.
    """
    is_updated = False

    # Check if we got a new and different email.
    if user_update.email is not None and user_update.email != current_user.email:
        is_updated = True

    # Check if the password changed. We do this by checking, whether the user can currently log in
    # with the new password. If that's the case, the password didn't change.
    if user_update.password is not None and user_update.password != current_user.email:
        user = crud.user.authenticate(
            email=current_user.username, password=user_update.password
        )
        if not user:
            # We cannot login -> the new password is different
            is_updated = True

    if not is_updated:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
        )

    crud.user.update(current_user, user_update)

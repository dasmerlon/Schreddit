from fastapi import APIRouter, HTTPException, status

from app import crud, schemas

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




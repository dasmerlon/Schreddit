from fastapi import APIRouter, HTTPException, status
from app import crud, schemas, models

router = APIRouter()


@router.post("/register",
             name="Register User",
             response_model=schemas.User,
             status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate):
    """
    Register a new user with a valid `email` address, a `username` and a `password`.
    """
    username_exists = crud.user.get_by_username(user.username)
    if username_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User with this username already exists.")
    email_exists = crud.user.get_by_email(user.email)
    if email_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User with this e-mail address already exists.")
    registered_user = crud.user.create(user)
    return registered_user

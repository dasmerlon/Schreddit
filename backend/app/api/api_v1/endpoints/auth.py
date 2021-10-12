from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from neomodel import DeflateError

from app import crud, schemas
from app.api.api_v1.exceptions import InvalidCredentialsException
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/login", name="Get an access token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Return a JWT access token for a user.

    The token is cached internally and is valid for 30 minutes.

    - `username`: email or username of the user
    - `password`: password of the user
    """
    # try to authenticate user with provided credentials
    try:
        user = crud.user.authenticate_by_email(form_data.username, form_data.password)
    except DeflateError:
        user = crud.user.authenticate_by_username(
            form_data.username, form_data.password
        )

    if not user:
        # The user credentials were invalid, return an error
        raise InvalidCredentialsException()

    # Create a new JWT with a fixed expiry date.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.uid, expires_delta=access_token_expires
    )

    # Save the access token with the linked user id in redis and return it to the user.
    crud.redis.set(access_token, user.uid)
    return {"access_token": access_token, "token_type": "bearer"}

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.sessions import redis

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Users can login via email+password.
    If everything succeeds, a new JWT will be created and returned.
    On top of that, we also save all JWTs in a Redis cache for faster lookup.
    """
    # Check if the user can login with the current email-password combination.
    user = crud.user.authenticate(form_data.username, form_data.password)

    if not user:
        # The user credentials were invalid, return an error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a new JWT with a fixed expiry date.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.uid, expires_delta=access_token_expires
    )

    # Save the access token with the linked user id in redis and return it to the user.
    redis.set(access_token, user.uid, ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return {"access_token": access_token, "token_type": "bearer"}

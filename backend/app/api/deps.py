from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app import crud, models, schemas
from app.api.api_v1.exceptions import InvalidCredentialsException
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    """
    This function checks the validity of a given Authentication Bearer token.
    If the token isn't expired and associated with an existing user,
    the user is then returned to calling function.

    If the credentials aren't valid, an unauthorized exception is thrown.
    """
    user_uuid = crud.redis.get(token)
    if user_uuid is None:
        user_uuid = get_user_id_from_jwt(token)
    else:
        user_uuid = user_uuid.decode("utf-8")

    user = crud.user.get(user_uuid)
    if user is None:
        raise InvalidCredentialsException()
    return user


def get_user_id_from_jwt(token: str) -> str:
    """
    Use the native logic to decode the JWT and return the user uuid if it succeeded.
    """
    try:
        # Decode the JWT payload
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.JWTError:
        raise InvalidCredentialsException()

    if payload.get("sub") is None:
        raise InvalidCredentialsException()

    # Get the decrypted token_data and extract the user uuid
    token_data = schemas.TokenPayload(**payload)
    return token_data.sub.replace(settings.SUB_PREFIX, "", 1)

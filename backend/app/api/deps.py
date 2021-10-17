from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app import crud, models, schemas
from app.api.api_v1.exceptions import InvalidCredentialsException
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False
)


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    """
    This function checks the validity of a given Authentication Bearer token.
    If the token isn't expired and associated with an existing user,
    the user is then returned to calling function.

    :param token: token to extract the user from
    :return: user associated with the token
    :raises InvalidCredentialsException: if the token cannot be decoded or is not
        associated with a user
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


def get_current_user_or_none(
    token: str = Depends(oauth2_scheme_optional),
) -> Optional[models.User]:
    """
    Check the validity of a JWT and return the associated user.

    :param token: JWT to extract the user from
    :return: user associated with the token or ``None`` if no token provided
    :raises InvalidCredentialsException: if the token cannot be decoded or is not
        associated with a user
    """
    if token:
        return get_current_user(token)
    else:
        return


def get_user_id_from_jwt(token: str) -> str:
    """
    Decode a JWT and return the UUID of the associated user.

    :param token: JWT to decode
    :return: UUID of the associated user
    :raises InvalidCredentialsException: if the token cannot be decoded or does not
        contain a ``sub`` field
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

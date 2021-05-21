from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app import crud, models, schemas
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("sub") is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(**payload)
    except jwt.JWTError:
        raise credentials_exception
    user = crud.user.get(token_data.sub.replace(settings.SUB_PREFIX, "", 1))
    if user is None:
        raise credentials_exception
    return user

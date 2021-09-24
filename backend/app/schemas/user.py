import re
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, validator

from app.core.config import settings


class UserBase(BaseModel):
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

    @validator("username")
    def username_limitations(cls, value):
        if (
            len(value) < settings.MIN_USERNAME_LENGTH
            or len(value) > settings.MAX_USERNAME_LENGTH
        ):
            raise ValueError(
                f"Username must be between {settings.MIN_USERNAME_LENGTH} and "
                f"{settings.MAX_USERNAME_LENGTH} characters."
            )
        elif not re.fullmatch(r"[\w-]+", value):
            raise ValueError(
                "Username must only consist of letters, numbers, dashes, "
                "and underscores."
            )
        else:
            return value


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    uid: UUID4
    username: str

    class Config:
        orm_mode = True

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
        if len(value) < 3 or len(value) > settings.MAX_USERNAME_LENGTH:
            raise ValueError(
                f"Username must be between 3 and {settings.MAX_USERNAME_LENGTH} "
                f"characters."
            )
        elif re.match("^[a-zA-Z0-9_-]+$", value) is None:
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

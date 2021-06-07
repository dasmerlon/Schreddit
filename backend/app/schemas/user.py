from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr

from app.schemas.base import PostGetterDict


class UserBase(BaseModel):
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    uid: UUID4
    username: str

    class Config:
        orm_mode = True
        getter_dict = PostGetterDict

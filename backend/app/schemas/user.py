from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    class Config:
        orm_mode = True

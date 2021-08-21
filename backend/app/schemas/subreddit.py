from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, UUID4

from app.core.config import settings
from app.schemas.base import SubredditGetterDict
from app.schemas.user import User


class SubredditType(str, Enum):
    archived = "archived"
    private = "private"
    public = "public"
    restricted = "restricted"
    user = "user"


class SubredditBase(BaseModel):
    description: Optional[str] = None
    # over_18: Optional[bool] = None
    # public_description: Optional[bool] = None
    # spoilers_enable: Optional[bool] = None
    title: Optional[str] = Query(None, max_length=settings.MAX_TITLE_LENGTH)
    # welcome_message_enabled: Optional[bool] = None
    # welcome_message_text: Optional[str] = None


class SubredditCreate(SubredditBase):
    description: str
    sr: str
    title: str = Query(None, max_length=settings.MAX_TITLE_LENGTH)
    type: SubredditType

    class Config:
        use_enum_values = True


class SubredditUpdate(SubredditBase):
    pass


class Subreddit(SubredditCreate):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    admin: User
    uid: UUID4

    class Config:
        orm_mode = True
        getter_dict = SubredditGetterDict

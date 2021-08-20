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
    # employees_only = "employees_only"
    # gold_only = "gold_only"
    # gold_restricted = "gold_restricted"
    private = "private"
    public = "public"
    restricted = "restricted"
    user = "user"


class SubredditBase(BaseModel):
    description: Optional[str] = None
    # over_18: Optional[bool] = None
    # public_description: Optional[bool] = None
    # spoilers_enable: Optional[bool] = None
    # sr: Optional[str] = None
    # submit_link_label: Optional[str] = None
    # submit_text_label: Optional[str] = None
    title: Optional[str] = Query(None, max_length=settings.MAX_TITLE_LENGTH)
    type: Optional[SubredditType] = None
    # welcome_message_enabled: Optional[bool] = None
    # welcome_message_text: Optional[str] = None


class SubredditCreate(SubredditBase):
    sr: str
    # submit_text: str
    title: str = Query(..., max_length=settings.MAX_TITLE_LENGTH)
    type: SubredditType

    class Config:
        use_enum_values = True


class SubredditUpdate(SubredditBase):
    pass


class Subreddit(SubredditCreate):
    created_at: Optional[datetime]
    admin: User
    uid: UUID4

    class Config:
        orm_mode = True
        getter_dict = SubredditGetterDict

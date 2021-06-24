from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import User


class SubredditType(str, Enum):
    archived = "archived"
    #employees_only = "employees_only"
    #gold_only = "gold_only"
    #gold_restricted = "gold_restricted"
    private = "private"
    public = "public"
    restricted = "restricted"
    user = "user"


class SubredditBase(BaseModel):
    description: Optional[str] = None
    #over_18: Optional[bool] = None
    #public_description: Optional[bool] = None
    #spoilers_enable: Optional[bool] = None
    sr: Optional[str] = None
    #submit_link_label: Optional[str] = None
    #submit_text_label: Optional[str] = None
    #welcome_message_enabled: Optional[bool] = None
    #welcome_message_text: Optional[str] = None


class SubredditCreate(SubredditBase):
    sr: str
    #submit_text: str
    title: str
    type: SubredditType


class SubredditUpdate(SubredditBase):
    pass


class Subreddit(SubredditCreate):
    created_at: Optional[datetime]
    admin: User

    class Config:
        orm_mode = True

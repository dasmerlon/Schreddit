import re
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import UUID4, BaseModel, constr, validator

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
    description: Optional[
        constr(min_length=1, max_length=settings.MAX_DESCRIPTION_LENGTH)
    ]
    # over_18: Optional[bool] = None
    # public_description: Optional[bool] = None
    # spoilers_enable: Optional[bool] = None
    title: Optional[constr(min_length=1, max_length=settings.MAX_TITLE_LENGTH)]
    # welcome_message_enabled: Optional[bool] = None
    # welcome_message_text: Optional[str] = None


class SubredditCreate(SubredditBase):
    description: constr(min_length=1, max_length=settings.MAX_DESCRIPTION_LENGTH)
    sr: str
    title: constr(min_length=1, max_length=settings.MAX_TITLE_LENGTH)
    type: SubredditType = SubredditType.public

    @validator("sr")
    def sr_limitations(cls, value):
        if len(value) < settings.MIN_SR_LENGTH or len(value) > settings.MAX_SR_LENGTH:
            raise ValueError(
                f"Subreddit name must be between {settings.MIN_SR_LENGTH} and "
                f"{settings.MAX_SR_LENGTH} characters."
            )
        elif not re.fullmatch(r"\w+", value):
            raise ValueError(
                "Subreddit name must only consist of letters, numbers, and underscores."
            )
        else:
            return value

    class Config:
        use_enum_values = True


class SubredditUpdate(SubredditBase):
    pass


class SubredditNoAdmin(SubredditCreate):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    uid: UUID4

    class Config:
        orm_mode = True
        getter_dict = SubredditGetterDict


class Subreddit(SubredditNoAdmin):
    admin: User


class SubredditList(BaseModel):
    subreddits: List[SubredditNoAdmin]

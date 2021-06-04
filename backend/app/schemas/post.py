from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import Query
from pydantic import UUID4, BaseModel, HttpUrl

from app.core.config import settings
from app.schemas.base import Pagination
from app.schemas.user import User


class PostSort(str, Enum):
    best = "best"
    hot = "hot"
    new = "new"
    top = "top"


class PostType(str, Enum):
    link = "link"
    self = "self"
    image = "image"
    video = "video"
    videogif = "videogif"


class PostBase(BaseModel):
    nsfw: Optional[bool] = None
    spoiler: Optional[bool] = None
    text: Optional[str] = None
    title: Optional[str] = Query(..., max_length=settings.MAX_TITLE_LENGTH)
    url: Optional[HttpUrl] = None


class PostCreate(PostBase):
    nsfw: bool
    spoiler: bool
    sr: str
    title: str = Query(..., max_length=settings.MAX_TITLE_LENGTH)
    type: PostType

    class Config:
        use_enum_values = True


class PostUpdate(PostBase):
    uid: UUID4


class Post(PostBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    type: PostType
    # sr: Subreddit TODO: uncomment when subreddit logic is implemented
    uid: UUID4
    author: User

    class Config:
        orm_mode = True


class PostList(BaseModel):
    pagination: Pagination
    results: List[Post]

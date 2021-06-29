from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.base import PostGetterDict
from app.schemas.subreddit import Subreddit
from app.schemas.user import User


class PostType(str, Enum):
    link = "link"
    self = "self"
    image = "image"
    video = "video"
    videogif = "videogif"


class PostMetaBase(BaseModel):
    nsfw: Optional[bool] = None
    spoiler: Optional[bool] = None


class PostMetaCreate(PostMetaBase):
    nsfw: bool
    spoiler: bool
    sr: str
    type: PostType

    class Config:
        use_enum_values = True


class PostMetaUpdate(PostMetaBase):
    pass


class PostMeta(PostMetaBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    type: PostType
    uid: UUID4
    author: Optional[User] = None
    subreddit: Subreddit

    class Config:
        orm_mode = True
        getter_dict = PostGetterDict

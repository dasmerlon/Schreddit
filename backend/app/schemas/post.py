from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, HttpUrl


class PostType(str, Enum):
    link = "link"
    self = "self"
    image = "image"
    video = "video"
    videogif = "videogif"


class PostBase(BaseModel):
    nsfw: bool
    spoiler: bool
    sr: str
    text: Optional[str] = None
    title: str = Query(..., max_length=300)
    type: PostType
    url: Optional[HttpUrl] = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: str
    user: str

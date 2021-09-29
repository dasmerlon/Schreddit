from enum import Enum
from typing import Optional

from app.schemas.base import PostGetterDict
from app.schemas.thing_meta import (ThingMeta, ThingMetaBase, ThingMetaCreate,
                                    ThingMetaUpdate)


class PostType(str, Enum):
    link = "link"
    self = "self"
    image = "image"
    video = "video"


class PostMetaBase(ThingMetaBase):
    nsfw: Optional[bool] = None
    spoiler: Optional[bool] = None


class PostMetaCreate(PostMetaBase, ThingMetaCreate):
    nsfw: bool
    spoiler: bool
    sr: str
    type: PostType

    class Config:
        use_enum_values = True


class PostMetaUpdate(PostMetaBase, ThingMetaUpdate):
    pass


class PostMeta(PostMetaBase, ThingMeta):
    type: PostType
    sr: str

    class Config:
        getter_dict = PostGetterDict

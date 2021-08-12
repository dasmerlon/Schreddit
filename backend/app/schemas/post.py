from enum import Enum
from typing import List

from pydantic import BaseModel, validator

from app.schemas.base import Pagination
from app.schemas.post_content import (PostContent, PostContentCreate,
                                      PostContentUpdate)
from app.schemas.post_meta import (PostMeta, PostMetaCreate, PostMetaUpdate,
                                   PostType)


class PostSort(str, Enum):
    best = "best"
    hot = "hot"
    new = "new"
    top = "top"


class PostCreate(BaseModel):
    metadata: PostMetaCreate
    content: PostContentCreate

    @validator("content")
    def check_content(cls, v, values):
        if "metadata" in values:
            if values["metadata"].type == PostType.link:
                assert v.text is None, "text must be None"
                assert v.url is not None, "url must not be None"
            elif values["metadata"].type == PostType.self:
                assert v.text is not None, "text must not be None"
                assert v.url is None, "url must be None"
        return v


class PostUpdate(BaseModel):
    metadata: PostMetaUpdate
    content: PostContentUpdate


class Post(BaseModel):
    metadata: PostMeta
    content: PostContent


class PostList(BaseModel):
    links: Pagination
    data: List[Post]

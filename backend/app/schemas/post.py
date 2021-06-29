from enum import Enum
from typing import List

from pydantic import BaseModel

from app.schemas.base import Pagination
from app.schemas.post_content import (PostContent, PostContentCreate,
                                      PostContentUpdate)
from app.schemas.post_meta import PostMeta, PostMetaCreate, PostMetaUpdate


class PostSort(str, Enum):
    best = "best"
    hot = "hot"
    new = "new"
    top = "top"


class PostCreate(BaseModel):
    metadata: PostMetaCreate
    content: PostContentCreate


class PostUpdate(BaseModel):
    metadata: PostMetaUpdate
    content: PostContentUpdate


class Post(BaseModel):
    metadata: PostMeta
    content: PostContent


class PostList(BaseModel):
    links: Pagination
    data: List[Post]

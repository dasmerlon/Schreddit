from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, validator

from app.schemas.base import Pagination
from app.schemas.comment import CommentTree
from app.schemas.post_content import (PostContent, PostContentCreate,
                                      PostContentUpdate)
from app.schemas.post_meta import (PostMeta, PostMetaCreate, PostMetaUpdate,
                                   PostType)
from app.schemas.thing import Thing, ThingCreate, ThingUpdate


class PostSort(str, Enum):
    """
    Enum for the sorting order of posts.

    - ``hot`` sorts comments from highest to lowest hot score, which is similar to
      ``top``, but also consideres post age
    - ``new`` sorts comments from newest to oldest creation date
    - ``top`` sorts posts from highest to lowest vote count (upvotes-downvotes)
    """

    hot = "hot"  # see medium.com article "How Reddit ranking algorithms work"
    new = "new"  # newest posts first
    top = "top"  # highest post score (upvotes-downvotes) first


class PostCreate(ThingCreate[PostMetaCreate, PostContentCreate]):
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


class PostUpdate(ThingUpdate[PostMetaUpdate, PostContentUpdate]):
    pass


class Post(Thing[PostMeta, PostContent]):
    pass


class PostList(BaseModel):
    links: Pagination
    data: List[Post]


class PostTree(Post):
    children: Optional[List[CommentTree]]

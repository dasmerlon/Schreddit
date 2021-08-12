from enum import Enum

from pydantic import BaseModel

from app.schemas.comment_content import (CommentContent, CommentContentCreate,
                                         CommentContentUpdate)
from app.schemas.comment_meta import CommentMeta


class CommentSort(str, Enum):
    confidence = "confidence"
    top = "top"
    new = "new"
    old = "old"
    # controversial = "controversial"
    # qa = "qa"


class CommentCreate(CommentContentCreate):
    pass


class CommentUpdate(CommentContentUpdate):
    pass


class Comment(BaseModel):
    metadata: CommentMeta
    content: CommentContent

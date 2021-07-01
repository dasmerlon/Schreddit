from enum import Enum

from pydantic import BaseModel

from app.schemas.comment_content import (CommentContent, CommentContentCreate,
                                         CommentContentUpdate)
from app.schemas.comment_meta import (CommentMeta, CommentMetaCreate,
                                      CommentMetaUpdate)


class CommentSort(str, Enum):
    confidence = "confidence"
    top = "top"
    new = "new"
    old = "old"
    # controversial = "controversial"
    # qa = "qa"


class CommentCreate(BaseModel):
    metadata: CommentMetaCreate
    content: CommentContentCreate


class CommentUpdate(BaseModel):
    metadata: CommentMetaUpdate
    content: CommentContentUpdate


class Comment(BaseModel):
    metadata: CommentMeta
    content: CommentContent

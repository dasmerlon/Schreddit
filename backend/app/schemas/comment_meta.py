from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.base import CommentGetterDict
from app.schemas.user import User


class CommentParentType(str, Enum):
    post = "post"
    comment = "comment"


class CommentMeta(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    uid: UUID4
    author: Optional[User] = None
    parent: UUID4

    class Config:
        orm_mode = True
        getter_dict = CommentGetterDict

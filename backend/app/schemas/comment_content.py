from typing import Optional

from pydantic import BaseModel


class CommentContentBase(BaseModel):
    text: Optional[constr(min_length=1, strip_whitespace=True)] = None


class CommentContentCreate(CommentContentBase):
    text: str


class CommentContentUpdate(CommentContentBase):
    pass


class CommentContent(CommentContentBase):
    class Config:
        orm_mode = True

from typing import Optional

from pydantic import BaseModel


class CommentContentBase(BaseModel):
    text: Optional[str] = None


class CommentContentCreate(CommentContentBase):
    text: str


class CommentContentUpdate(CommentContentBase):
    pass


class CommentContent(CommentContentBase):
    class Config:
        orm_mode = True

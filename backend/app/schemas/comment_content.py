from typing import Optional

from pydantic import BaseModel, constr, validator


class CommentContentBase(BaseModel):
    text: Optional[constr(min_length=1, strip_whitespace=True)] = None

    @validator("text")
    def text_must_not_be_none(cls, v):
        if v is None:
            raise ValueError("text must not be None")
        else:
            return v


class CommentContentCreate(CommentContentBase):
    text: constr(min_length=1, strip_whitespace=True)


class CommentContentUpdate(CommentContentBase):
    pass


class CommentContent(CommentContentBase):
    class Config:
        orm_mode = True

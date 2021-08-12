from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, constr, validator

from app.core.config import settings


class PostContentBase(BaseModel):
    text: Optional[constr(min_length=1, strip_whitespace=True)] = None
    title: Optional[
        constr(
            min_length=1, max_length=settings.MAX_TITLE_LENGTH, strip_whitespace=True
        )
    ]
    url: Optional[HttpUrl] = None

    @validator("title")
    def title_must_not_be_none(cls, v):
        if v is None:
            raise ValueError("title must not be None")
        else:
            return v


class PostContentCreate(PostContentBase):
    title: constr(
        min_length=1, max_length=settings.MAX_TITLE_LENGTH, strip_whitespace=True
    )


class PostContentUpdate(PostContentBase):
    pass


class PostContent(PostContentBase):
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

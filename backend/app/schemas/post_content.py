from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, HttpUrl

from app.core.config import settings


class PostContentBase(BaseModel):
    text: Optional[str] = None
    title: Optional[str] = Query(..., max_length=settings.MAX_TITLE_LENGTH)
    url: Optional[HttpUrl] = None


class PostContentCreate(PostContentBase):
    title: str = Query(..., max_length=settings.MAX_TITLE_LENGTH)


class PostContentUpdate(PostContentBase):
    pass


class PostContent(PostContentBase):
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

from typing import Optional

from pydantic import HttpUrl, constr, validator

from app.core.config import settings
from app.schemas.thing_content import (ThingContent, ThingContentBase,
                                       ThingContentCreate, ThingContentUpdate)


class PostContentBase(ThingContentBase):
    title: Optional[
        constr(
            min_length=1, max_length=settings.MAX_TITLE_LENGTH, strip_whitespace=True
        )
    ] = None
    url: Optional[HttpUrl] = None

    @validator("title")
    def title_must_not_be_none(cls, v):
        if v is None:
            raise ValueError("title must not be None")
        else:
            return v


class PostContentCreate(PostContentBase, ThingContentCreate):
    title: constr(
        min_length=1, max_length=settings.MAX_TITLE_LENGTH, strip_whitespace=True
    )


class PostContentUpdate(PostContentBase, ThingContentUpdate):
    pass


class PostContent(PostContentBase, ThingContent):
    pass

from pydantic import validator

from app.schemas.thing_content import (ThingContent, ThingContentBase,
                                       ThingContentCreate, ThingContentUpdate)


class CommentContentBase(ThingContentBase):
    @validator("text")
    def text_must_not_be_none(cls, v):
        if v is None:
            raise ValueError("text must not be None")
        return v


class CommentContentCreate(CommentContentBase, ThingContentCreate):
    pass


class CommentContentUpdate(CommentContentBase, ThingContentUpdate):
    pass


class CommentContent(CommentContentBase, ThingContent):
    pass

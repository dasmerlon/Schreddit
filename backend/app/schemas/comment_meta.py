from pydantic import UUID4

from app.schemas.base import CommentGetterDict
from app.schemas.thing_meta import (ThingMeta, ThingMetaBase, ThingMetaCreate,
                                    ThingMetaUpdate)


class CommentMetaBase(ThingMetaBase):
    pass


class CommentMetaCreate(CommentMetaBase, ThingMetaCreate):
    pass


class CommentMetaUpdate(CommentMetaBase, ThingMetaUpdate):
    pass


class CommentMetaNoParent(CommentMetaBase, ThingMeta):
    pass


class CommentMeta(CommentMetaBase, ThingMeta):
    parent: UUID4

    class Config:
        getter_dict = CommentGetterDict

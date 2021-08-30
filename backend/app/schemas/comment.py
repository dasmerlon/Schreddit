from enum import Enum

from app.schemas.comment_content import (CommentContent, CommentContentCreate,
                                         CommentContentUpdate)
from app.schemas.comment_meta import (CommentMeta, CommentMetaCreate,
                                      CommentMetaUpdate)
from app.schemas.thing import Thing, ThingCreate, ThingUpdate


class CommentSort(str, Enum):
    confidence = "confidence"
    top = "top"
    new = "new"
    old = "old"
    # controversial = "controversial"
    # qa = "qa"


class CommentCreate(ThingCreate[CommentMetaCreate, CommentContentCreate]):
    pass


class CommentUpdate(ThingUpdate[CommentMetaUpdate, CommentContentUpdate]):
    pass


class Comment(Thing[CommentMeta, CommentContent]):
    pass

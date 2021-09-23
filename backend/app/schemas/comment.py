from enum import Enum
from typing import ForwardRef, List, Optional

from app.schemas.comment_content import (CommentContent, CommentContentCreate,
                                         CommentContentUpdate)
from app.schemas.comment_meta import (CommentMeta, CommentMetaCreate,
                                      CommentMetaNoParent, CommentMetaUpdate)
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


class CommentNoParent(Thing[CommentMetaNoParent, CommentContent]):
    pass


CommentTree = ForwardRef("CommentTree")


class CommentTree(CommentNoParent):
    children: Optional[List[CommentTree]]


CommentTree.update_forward_refs()

from neomodel import db

from app.crud.crud_thing_meta import CRUDThingBaseMeta
from app.models import CommentMeta, ThingMeta
from app.schemas import CommentMetaCreate, CommentMetaUpdate


class CRUDCommentMeta(
    CRUDThingBaseMeta[CommentMeta, CommentMetaCreate, CommentMetaUpdate]
):
    """Comment meta class for CRUD operations"""

    @db.write_transaction
    def set_parent(self, db_obj: CommentMeta, parent: ThingMeta) -> ThingMeta:
        comment_parent = db_obj.parent.connect(parent)
        return comment_parent


comment_meta = CRUDCommentMeta(CommentMeta)

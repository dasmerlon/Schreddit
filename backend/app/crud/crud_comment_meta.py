from neomodel import db

from app.crud.crud_thing_meta import CRUDThingBaseMeta
from app.models import CommentMeta, ThingMeta
from app.schemas import CommentMetaCreate, CommentMetaUpdate


class CRUDCommentMeta(
    CRUDThingBaseMeta[CommentMeta, CommentMetaCreate, CommentMetaUpdate]
):
    """CRUD class for comment metadata"""

    @db.write_transaction
    def set_parent(self, db_obj: CommentMeta, parent: ThingMeta) -> None:
        """
        Set the parent of a comment.

        :param db_obj: node of the comment whose parent will be set
        :param parent: the parent node of the comment
        """
        db_obj.parent.connect(parent)


comment_meta = CRUDCommentMeta(CommentMeta)

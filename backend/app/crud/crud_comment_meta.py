from neomodel import db

from app.crud.base_neo import CRUDBaseNeo
from app.models import CommentMeta, Thing, User
from app.schemas import CommentMetaCreate, CommentMetaUpdate


class CRUDCommentMeta(CRUDBaseNeo[CommentMeta, CommentMetaCreate, CommentMetaUpdate]):
    """Comment class for CRUD operations"""

    @db.write_transaction
    def set_author(self, db_obj: CommentMeta, author: User) -> User:
        post_author = db_obj.author.connect(author)
        return post_author

    @db.write_transaction
    def set_parent(self, db_obj: CommentMeta, parent: Thing) -> Thing:
        post_parent = db_obj.parent.connect(parent)
        return post_parent


comment_meta = CRUDCommentMeta(CommentMeta)

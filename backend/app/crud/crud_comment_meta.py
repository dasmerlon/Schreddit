from neomodel import db
from pydantic import BaseModel

from app.crud.base_neo import CRUDBaseNeo
from app.models import CommentMeta, Thing, User


class CRUDCommentMeta(CRUDBaseNeo[CommentMeta, BaseModel, BaseModel]):
    """Comment class for CRUD operations"""

    @db.read_transaction
    def get_author(self, db_obj: CommentMeta) -> User:
        return db_obj.author.single()

    @db.write_transaction
    def set_author(self, db_obj: CommentMeta, author: User) -> User:
        comment_author = db_obj.author.connect(author)
        return comment_author

    @db.write_transaction
    def set_parent(self, db_obj: CommentMeta, parent: Thing) -> Thing:
        comment_parent = db_obj.parent.connect(parent)
        return comment_parent


comment_meta = CRUDCommentMeta(CommentMeta)

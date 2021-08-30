from neomodel import db

from app.crud.base_neo import (CreateSchemaType, CRUDBaseNeo, ModelType,
                               UpdateSchemaType)
from app.models import ThingMeta, User
from app.schemas import ThingMetaCreate, ThingMetaUpdate


class CRUDThingBaseMeta(CRUDBaseNeo[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Thing meta abstract base class"""

    @db.read_transaction
    def get_author(self, db_obj: ThingMeta) -> User:
        return db_obj.author.single()

    @db.write_transaction
    def set_author(self, db_obj: ThingMeta, author: User) -> User:
        return db_obj.author.connect(author)


thing_meta = CRUDThingBaseMeta[ThingMeta, ThingMetaCreate, ThingMetaUpdate](ThingMeta)

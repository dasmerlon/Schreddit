from datetime import datetime, timezone
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from neomodel import NodeSet, StructuredNode, db
from pydantic import UUID4, BaseModel

ModelType = TypeVar("ModelType", bound=StructuredNode)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBaseNeo(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Abstract base class for CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        :param model: a neomodel model class
        """
        self.model = model

    @db.read_transaction
    def get(self, uid: Union[str, UUID4]) -> Optional[ModelType]:
        """
        Get one node from the model class.
        :param uid: the unique identifier of the node to get
        :return: the requested node if it exists, else None
        """
        if isinstance(uid, UUID):
            return self.model.nodes.get_or_none(uid=uid.hex)
        else:
            return self.model.nodes.get_or_none(uid=uid)

    @db.read_transaction
    def get_all(self) -> NodeSet:
        """
        Get an Iterable of all nodes from the model class.

        :return: iterable of nodes
        """
        return self.model.nodes

    @db.write_transaction
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new node.

        :param obj_in: the CreateSchema of the node to create
        :return: the database model of the created node
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db_obj.save()
        return db_obj

    @db.write_transaction
    def update(
        self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any], None]
    ) -> ModelType:
        """
        Update a node.

        :param db_obj: the database model of the node to be updated
        :param obj_in: the UpdateSchema of the node to be updated
        :return: the updated database model
        """
        # convert obj_in to a dict
        if isinstance(obj_in, dict):
            update_data = obj_in
        elif obj_in is None:  # no update data, only update timestamp
            update_data = {}
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # update fields
        for field in db_obj.__properties__:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        # update timestamp if it exists
        if hasattr(db_obj, "updated_at"):
            setattr(db_obj, "updated_at", datetime.now(timezone.utc))

        db_obj.save()
        return db_obj

    @db.write_transaction
    def remove(self, uid: Union[str, UUID4]) -> Optional[ModelType]:
        """
        Remove a node.
        :param uid: the unique identifier of the node to be removed
        :return: the removed node
        """
        if isinstance(uid, UUID):
            obj = self.model.nodes.get_or_none(uid=uid.hex)
        else:
            obj = self.model.nodes.get_or_none(uid=uid)

        if obj is not None:
            obj.delete()
        return obj

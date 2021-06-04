from datetime import datetime, timezone
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from neomodel import NodeSet, StructuredNode, UniqueIdProperty, db
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=StructuredNode)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Abstract base class for CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        :param model: a neomodel model class
        """
        self.model = model

    @db.read_transaction
    def get(self, uid: UniqueIdProperty) -> Optional[ModelType]:
        """
        Get one node from the model class.
        :param uid: the unique identifier of the node to get
        :return: the requested node if it exists, else None
        """
        return self.model.nodes.get_or_none(uid=uid)

    @db.read_transaction
    def get_all(self) -> NodeSet:
        """
        Get an Iterable of all nodes from the model class.
        :return: iterable of nodes
        """
        return self.model.nodes

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
        self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a node.
        :param db_obj: the database model of the node to be updated
        :param obj_in: the UpdateSchema of the node to be updated
        :return: the updated database model
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in db_obj.serialize:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if hasattr(db_obj, "updated_at"):
            setattr(db_obj, "updated_at", datetime.now(timezone.utc))
        db_obj.save()
        return db_obj

    @db.write_transaction
    def remove(self, uid: UniqueIdProperty) -> Optional[ModelType]:
        """
        Remove a node.
        :param uid: the unique identifier of the node to be removed
        :return: the removed node
        """
        obj = self.model.nodes.get(uid=uid)
        obj.delete()
        return obj

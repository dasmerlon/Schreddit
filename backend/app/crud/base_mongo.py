from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from mongoengine import Document, QuerySet
from pydantic import UUID4, BaseModel

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBaseMongo(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Abstract base class for CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        :param model: mongodb model class
        """
        self.model = model

    def get(self, uid: Union[str, UUID4]) -> Optional[ModelType]:
        """
        Get one document from the model class.

        :param uid: UUID of the document to get
        :return: the requested document if it exists, else None
        """
        if isinstance(uid, UUID):
            return self.model.objects(uid=uid.hex).first()
        else:
            return self.model.objects(uid=uid).first()

    def get_all(self) -> QuerySet:
        """
        Get all documents as a QuerySet from the model class.

        :return: QuerySet of documents
        """
        return self.model.objects

    def create(self, uid: Union[str, UUID4], obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new document.

        :param uid: UUID of associated metadata
        :param obj_in: ``CreateSchema`` of the document to create
        :return: the database model of the created document
        """
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["uid"] = uid
        db_obj = self.model(**obj_in_data)
        db_obj.save()
        return db_obj

    def update(
        self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a document.

        :param db_obj: database model object of the document to be updated
        :param obj_in: ``UpdateSchema`` or ``dict`` with updated data
        :return: the updated document
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        db_obj.update(**update_data)
        return db_obj

    def remove(self, uid: Union[str, UUID4]) -> Optional[ModelType]:
        """
        Remove a document.

        :param uid: UUID of the document to be removed
        :return: the removed document
        """
        if isinstance(uid, UUID):
            obj = self.model.objects(uid=uid.hex).first()
        else:
            obj = self.model.objects(uid=uid).first()

        if obj is not None:
            obj.delete()
        return obj

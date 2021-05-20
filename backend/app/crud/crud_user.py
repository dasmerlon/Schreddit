from typing import Any, Dict, Optional, Union
from pydantic import EmailStr
from neomodel import db
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """User class for CRUD operations."""

    @db.read_transaction
    def get_by_email(self, email: EmailStr) -> Optional[User]:
        """
        Get a user node by email.
        :param email: email of the user to get
        :return: the user if it exists, else `None`
        """
        return User.nodes.get_or_none(email=email)

    @db.read_transaction
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username.
        :param username: username of the user to get
        :return: the user if it exists, else `None`
        """
        return User.nodes.get_or_none(username=username)

    @db.write_transaction
    def create(self, obj_in: UserCreate) -> User:
        """
        Create a new user.
        :param obj_in: the `UserCreate` schema
        :return: the `User` model of the created user
        """
        hashed_password = obj_in.password  # TODO: hash password
        db_obj = self.model(email=obj_in.email,
                            username=obj_in.username,
                            hashed_password=hashed_password)
        db_obj.save()
        return db_obj

    @db.write_transaction
    def update(self, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        """
        Update an existing user
        :param db_obj: the model class of the user to update
        :param obj_in: the `UserUpdate` schema or a dict containing the updated data
        :return: the `User` model of the updated user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = obj_in.password  # TODO: hash password
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(User)

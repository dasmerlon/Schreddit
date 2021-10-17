from typing import Any, Dict, List, Optional, Union

from neomodel import db
from pydantic import EmailStr

from app.core.security import get_password_hash, verify_password
from app.crud.base_neo import CRUDBaseNeo
from app.models import Subreddit, User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBaseNeo[User, UserCreate, UserUpdate]):
    """CRUD class for users"""

    @db.read_transaction
    def get_by_email(self, email: EmailStr) -> Optional[User]:
        """
        Get a user node by email.

        :param email: email of the user to get
        :return: the user if it exists, else ``None``
        """
        return User.nodes.get_or_none(email=email)

    @db.read_transaction
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username.

        :param username: username of the user to get
        :return: the user if it exists, else ``None``
        """
        return User.nodes.get_or_none(username=username)

    @db.write_transaction
    def create(self, obj_in: UserCreate) -> User:
        """
        Create a new user. The plain-text password is hashed and then saved.

        :param obj_in: the ``UserCreate`` schema
        :return: the node of the created user
        """
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=hashed_password,
        )
        db_obj.save()
        return db_obj

    def update(self, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        """
        Update an existing user.

        :param db_obj: the node of the user to update
        :param obj_in: the ``UserUpdate`` schema or a dict containing the updated data
        :return: the node of the updated user
        """
        # Convert object to dictionary, so we have a consistent way of accessing fields.
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        # If the password is updated, create a password hash and persist it.
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db_obj, update_data)

    def authenticate_by_email(self, email: EmailStr, password: str) -> Optional[User]:
        """
        Authenticate a user by email.

        :param email: email of the user
        :param password: password of the user
        :return: the node of the user, if a user with the email exists and the password
            is correct, else ``None``
        """
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def authenticate_by_username(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username.

        :param username: username of the user
        :param password: password of the user
        :return: the node of the user, if a user with the email exists and the password
            is correct, else ``None``
        """
        user = self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @db.read_transaction
    def get_subscriptions(self, db_obj: User) -> List[Subreddit]:
        """
        Get all subreddit subscriptions of a user.

        :param db_obj: user node
        :return: list of all subreddit nodes the user is subscribed to
        """
        return db_obj.subscription.order_by("sr").all()

    @db.read_transaction
    def get_recommendations(self, db_obj: User, limit: int) -> List[Subreddit]:
        """
        Get recommended subreddits for a user.

        :param db_obj: user node
        :param limit: maximum number of recommended subreddits
        :return: list of all subreddit nodes that are recommended to the user, sorted by
            a score of relevance
        """
        query = (
            "MATCH (user:User)-[:SUBSCRIBED_TO*3]-(s:Subreddit) "
            "WHERE user.uid = $user_uid AND NOT exists((user)-[:SUBSCRIBED_TO]-(s)) "
            "RETURN s, count(*) as occurrence "
            "ORDER BY occurrence DESC "
            "LIMIT $limit"
        )
        params = {"user_uid": db_obj.uid, "limit": limit}
        results, columns = db.cypher_query(query, params)
        return [Subreddit.inflate(row[0]) for row in results]


user = CRUDUser(User)

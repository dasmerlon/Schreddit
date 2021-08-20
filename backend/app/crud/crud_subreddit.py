from typing import Optional

from neomodel import db

from app.crud.base_neo import CRUDBaseNeo
from app.models import Subreddit, User
from app.schemas import SubredditCreate, SubredditUpdate


class CRUDSubreddit(CRUDBaseNeo[Subreddit, SubredditCreate, SubredditUpdate]):
    """Subreddits class for CRUD operations"""

    @db.write_transaction
    def set_admin(self, db_obj: Subreddit, admin: User) -> User:
        sr_admin = db_obj.admin.connect(admin)
        return sr_admin

    @db.read_transaction
    def get_by_sr(self, sr: str) -> Optional[Subreddit]:
        """
        Get a Subreddit by sr.
        :param sr: name/sr of the subreddit
        :return: the subreddit, if it exists, else `None`
        """
        return Subreddit.nodes.get_or_none(sr=sr)

    @db.read_transaction
    def get_admin(self, db_obj: Subreddit) -> User:
        return db_obj.admin.single()

    # @db.write_transaction
    # def create(self, obj_in: Subreddit) -> Subreddit:
    #     """
    #     Create a subreddit.
    #     :param obj_in: the `SubredditCreate` schema
    #     :return: the created subreddit
    #     """
    #     db_obj = Subreddit(
    #         sr = obj_in.sr,
    #         title = obj_in.title,
    #         type = obj_in.type,
    #     )
    #     db_obj.save()
    #     return db_obj

    # @db.write_transaction
    # def update(self, admin: User, obj_in: Subreddit) -> Subreddit:
    #     """
    #     Update an existing subreddit.
    #     :param db_obj: the admin of the Subreddit
    #     :param obj_in: the `SubredditUpdate` schema to update
    #     :return: the updated subreddit
    #     """
    #     pass


subreddit = CRUDSubreddit(Subreddit)

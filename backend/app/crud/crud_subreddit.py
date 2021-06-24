from typing import Optional

from neomodel import db

from app.crud.base import CRUDBase
from app.models import Subreddit, User
from app.schemas import SubredditCreate, SubredditUpdate


class CRUDSubreddit(CRUDBase[Subreddit, SubredditCreate, SubredditUpdate]):
    """Subreddits class for CRUD operations"""

    @db.write_transaction
    def create(self, obj_in: SubredditCreate) -> Subreddit:
        """
        Create a new Subreddit.
        :param obj_in: the `SubredditCreate` schema
        :param admin: the admin of the Subreddit
        :return: the `Subreddit` model of the created Subreddit
        """
        db_obj = Subreddit(
            description=obj_in.description,
            sr=obj_in.sr,
            title=obj_in.title,
            type=obj_in.type.value,
        )
        db_obj.save()
        return db_obj

    @db.write_transaction
    def set_admin(self, db_obj: Subreddit, admin: User) -> User:
        db_obj.admin.connect(admin)
        return db_obj.admin.single()

    @db.read_transaction
    def get_by_sr(self, sr: str) -> Optional[Subreddit]:
        """
        Get a Subreddit by sr.
        :param sr: name/sr of the subreddit
        :return: the subreddit, if it exists, else `None`
        """
        return Subreddit.nodes.get_or_none(sr=sr)


subreddit = CRUDSubreddit(Subreddit)

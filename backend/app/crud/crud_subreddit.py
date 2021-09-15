from typing import List, Optional

from neomodel import db, Q

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
    def search(self, q: str, include_title: bool) -> List[Subreddit]:
        """
        Search a subreddit.

        :param q: the search string
        :param include_title: ``True`` if the subreddit titles should also be searched
        :return: a list of matching subreddits
        """
        if include_title:
            return Subreddit.nodes.filter(Q(sr__contains=q) | Q(title__contains=q)).all()
        else:
            return Subreddit.nodes.filter(Q(sr__contains=q)).all()

    @db.read_transaction
    def get_admin(self, db_obj: Subreddit) -> User:
        return db_obj.admin.single()


subreddit = CRUDSubreddit(Subreddit)

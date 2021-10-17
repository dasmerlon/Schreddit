from typing import List, Optional

from neomodel import Q, db

from app.crud.base_neo import CRUDBaseNeo
from app.models import Subreddit, User
from app.schemas import SubredditCreate, SubredditUpdate


class CRUDSubreddit(CRUDBaseNeo[Subreddit, SubredditCreate, SubredditUpdate]):
    """CRUD class for subreddits"""

    @db.write_transaction
    def set_admin(self, db_obj: Subreddit, admin: User) -> None:
        """
        Set the admin of a subreddit.

        :param db_obj: subreddit node
        :param admin: user node of the admin
        """
        db_obj.admin.connect(admin)

    @db.read_transaction
    def get_by_sr(self, sr: str) -> Optional[Subreddit]:
        """
        Get a subreddit by its name.

        :param sr: name of the subreddit
        :return: the subreddit, if it exists, else ``None``
        """
        return Subreddit.nodes.get_or_none(sr=sr)

    @db.read_transaction
    def search(self, q: str, include_title: bool) -> List[Subreddit]:
        """
        Search for a subreddit.

        :param q: the search string
        :param include_title: ``True`` if the subreddit titles should be included in the
            search
        :return: a list of matching subreddits
        """
        if include_title:
            return Subreddit.nodes.filter(
                Q(sr__contains=q) | Q(title__contains=q)
            ).all()
        else:
            return Subreddit.nodes.filter(Q(sr__contains=q)).all()

    @db.read_transaction
    def get_admin(self, db_obj: Subreddit) -> User:
        """
        Get the admin of a subreddit.

        :param db_obj: subreddit node
        :return: user node of the admin
        """
        return db_obj.admin.single()

    @db.write_transaction
    def set_subscription(self, db_obj: Subreddit, user: User) -> Subreddit:
        """
        Subscribe a user to a subreddit.

        :param db_obj: the subreddit that should be subscribed
        :param user: the user that should be subscribed to the subreddit
        """
        subscribed_subreddit = db_obj.subscriber.connect(user)
        return subscribed_subreddit

    @db.write_transaction
    def end_subscription(self, db_obj: Subreddit, user: User) -> Subreddit:
        """
        Unsubscribe a user from a subreddit.

        :param db_obj: the subreddit that should be unsubscribed
        :param user: the user that should be unsubscribed from the subreddit
        """
        unsubscribed_subreddit = db_obj.subscriber.disconnect(user)
        return unsubscribed_subreddit

    @db.read_transaction
    def get_subscriber_count(self, db_obj: Subreddit) -> int:
        """
        Get the subscriber count of a subreddit.

        :param db_obj: the subreddit whose subscriber count should be returned
        :return: the subscriber count of the subreddit
        """
        return len(db_obj.subscriber)

    @db.read_transaction
    def is_subscribed(self, db_obj: Subreddit, user: User):
        """
        Return the subscription state of a subreddit for a user.

        :param db_obj: the subreddit whose subscription state should be returned
        :param user: the user for whom the subscription state should be returned
        :return: ``True`` if the user is subscribed to the subreddit, else ``False``
        """
        return db_obj.subscriber.is_connected(user)


subreddit = CRUDSubreddit(Subreddit)

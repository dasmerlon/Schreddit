from typing import Optional

from neomodel import NodeSet, db

from app.crud.base_neo import CRUDBaseNeo
from app.models import PostMeta, Subreddit, User
from app.schemas import PostMetaCreate, PostMetaUpdate, PostSort


class CRUDPostMeta(CRUDBaseNeo[PostMeta, PostMetaCreate, PostMetaUpdate]):
    """Post class for CRUD operations"""

    @db.read_transaction
    def get_posts_after(
        self, after: Optional[PostMeta], sort: PostSort, limit: int
    ) -> NodeSet:
        """
        Get the posts after the cursor.

        :param after: get posts after this cursor according to the sorting   order,
        or get first posts if no cursor is specified
        :param sort: sorting order
        :param limit: number of posts to get
        :return: a list of posts
        """
        if sort.new:
            if after is None:
                result = self.model.nodes.order_by("-created_at")
            else:
                result = self.model.nodes.order_by("-created_at").filter(
                    created_at__lt=after.created_at
                )
        elif sort.hot:  # TODO: implement other sorting orders
            pass
        elif sort.top:
            pass
        elif sort.best:
            pass

        return result[:limit]

    @db.read_transaction
    def get_posts_before(self, before: PostMeta, sort: PostSort, limit: int) -> NodeSet:
        """
        Get the posts before the cursor.

        :param before: get posts before this cursor according to the sorting order
        :param sort: sorting order
        :param limit: number of posts to get
        :return: a list of posts
        """
        if sort.new:
            result = self.model.nodes.order_by("created_at").filter(
                created_at__gt=before.created_at
            )
        elif sort.hot:  # TODO: implement other sorting orders
            pass
        elif sort.top:
            pass
        elif sort.best:
            pass

        return result[:limit]

    @db.write_transaction
    def set_author(self, db_obj: PostMeta, author: User) -> User:
        post_author = db_obj.author.connect(author)
        return post_author

    @db.write_transaction
    def set_subreddit(self, db_obj: PostMeta, subreddit: Subreddit) -> Subreddit:
        post_subreddit = db_obj.subreddit.connect(subreddit)
        return post_subreddit


post_meta = CRUDPostMeta(PostMeta)

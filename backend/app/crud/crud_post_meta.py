from typing import Optional

from neomodel import NodeSet, db

from app.crud.crud_thing_meta import CRUDThingBaseMeta
from app.models import PostMeta, Subreddit
from app.schemas import PostMetaCreate, PostMetaUpdate, PostSort


class CRUDPostMeta(CRUDThingBaseMeta[PostMeta, PostMetaCreate, PostMetaUpdate]):
    """Post meta class for CRUD operations"""

    @db.read_transaction
    def get_posts_after(
        self,
        subreddit: Subreddit,
        after: Optional[PostMeta],
        sort: PostSort,
        limit: int,
    ) -> NodeSet:
        """
        Get the posts after the cursor.

        :param subreddit: the subreddit to get posts from
        :param after: get posts after this cursor according to the sorting order,
        or get first posts if no cursor is specified
        :param sort: sorting order
        :param limit: number of posts to get
        :return: a list of posts
        """
        if sort.new:
            if after is None:
                result = subreddit.post.order_by("-created_at")
            else:
                result = subreddit.post.order_by("-created_at").filter(
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
    def get_posts_before(
        self, subreddit: Subreddit, before: PostMeta, sort: PostSort, limit: int
    ) -> NodeSet:
        """
        Get the posts before the cursor.

        :param subreddit: the subreddit to get posts from
        :param before: get posts before this cursor according to the sorting order
        :param sort: sorting order
        :param limit: number of posts to get
        :return: a list of posts
        """
        if sort.new:
            result = subreddit.post.order_by("created_at").filter(
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
    def set_subreddit(self, db_obj: PostMeta, subreddit: Subreddit) -> Subreddit:
        post_subreddit = db_obj.subreddit.connect(subreddit)
        return post_subreddit


post_meta = CRUDPostMeta(PostMeta)

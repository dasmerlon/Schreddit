from neomodel import NodeSet, UniqueIdProperty, db
from pydantic import UUID4

from app.crud.base import CRUDBase
from app.models import Post, User, Subreddit
from app.schemas import PostCreate, PostSort, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    """Post class for CRUD operations"""

    def get_selection(
        self, after: UUID4, before: UUID4, sort: PostSort, limit: int
    ) -> NodeSet:
        """
        Get a selection of posts.
        :param after: get posts that were created after this post given by his uid
        :param before: get posts that were created before this post given by his uid
        :param limit: number of posts to get
        :return: a list of posts
        """
        if after is not None:
            cursor = self.get(after.hex)
        elif before is not None:
            cursor = self.get(before.hex)
        else:
            cursor = None

        if sort.new:
            if cursor is None:  # no cursor specified, start from the top
                cursor = self.model.nodes.order_by("-created_at").first_or_none()
            if cursor is None:  # queried nodeset is empty
                return []

            if before is not None:  # posts newer than or equal to cursor
                result = self.model.nodes.order_by("created_at").filter(
                    created_at__gte=cursor.created_at
                )
            else:  # posts older than or equal to cursor
                result = self.model.nodes.order_by("-created_at").filter(
                    created_at__lte=cursor.created_at
                )
            return result[:limit]
        elif sort.hot:  # TODO: implement other sorting orders
            pass
        elif sort.top:
            pass
        elif sort.best:
            pass

    @db.read_transaction
    def get_new_cursors(
        self, nodes: NodeSet, sort: PostSort
    ) -> (UniqueIdProperty, UniqueIdProperty):
        """
        Get new cursors for navigation.
        :param nodes: the nodeset that the cursors should be retrieved for
        :param sort: the sorting that was used for the nodeset
        :return:
        """
        if sort.new:
            after = (
                self.model.nodes.order_by("-created_at")
                .filter(created_at__lt=nodes[-1].created_at)
                .first_or_none()
            )
            before = (
                self.model.nodes.order_by("created_at")
                .filter(created_at__gt=nodes[0].created_at)
                .first_or_none()
            )
            return (after.uid if after else None, before.uid if before else None)

    @db.write_transaction
    def create(self, obj_in: PostCreate, author: User) -> Post:
        """
        Create a new post.
        :param obj_in: the `UserCreate` schema
        :param author: the author of the post
        :return: the `Post` model of the created post
        """
        db_obj = super().create(obj_in)
        db_obj.author.connect(author)
        return db_obj


post = CRUDPost(Post)

from datetime import datetime

from neomodel import NodeSet, db

from app.crud.base import CRUDBase
from app.models import Post, User
from app.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    """Post class for CRUD operations"""

    @db.read_transaction
    def get_selection(self, after: datetime, before: datetime, limit) -> NodeSet:
        """
        Get a selection of posts.
        :param after: get posts that were created after this Unix timestamp
        :param before: get posts that were created before this Unix timestamp
        :param limit: number of posts to get
        :return: a list of posts
        """
        if after:
            result = self.model.nodes.filter(created_at__lt=after)
        elif before:
            result = self.model.nodes.filter(created_at__gt=before)
        else:
            result = self.model.nodes
        return result.order_by("-created_at")[:limit]

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

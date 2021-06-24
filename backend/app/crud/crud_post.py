from neomodel import db

from app.crud.base import CRUDBase
from app.models import Post, User, Subreddit
from app.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    """Post class for CRUD operations"""

    @db.write_transaction
    def create(self, obj_in: PostCreate) -> Post:
        """
        Create a new post.
        :param obj_in: the `UserCreate` schema
        :param author: the author of the post
        :return: the `Post` model of the created post
        """
        db_obj = Post(
            nsfw=obj_in.nsfw,
            spoiler=obj_in.spoiler,
            text=obj_in.text,
            title=obj_in.title,
            type=obj_in.type.value,
            url=obj_in.url
        )
        db_obj.save()
        return db_obj

    @db.write_transaction
    def set_author(self, db_obj: Post, author: User) -> User:
        db_obj.author.connect(author)
        return db_obj.author.single()

    @db.write_transaction
    def set_subreddit(self, *, db_obj: Post, subreddit: Subreddit) -> Subreddit:
        db_obj.subreddit.connect(subreddit)
        return db_obj.subreddit.single()

post = CRUDPost(Post)
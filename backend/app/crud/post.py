from neomodel import db
from app.models import Post
from app.schemas import PostCreate


@db.write_transaction
def create(post: PostCreate):
    # add post to DB
    return post

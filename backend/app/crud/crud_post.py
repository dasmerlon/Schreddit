from neomodel import db
from app.models import Post
from app.schemas import PostCreate, PostUpdate
from app.crud.base import CRUDBase


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    pass

post = CRUDPost(Post)
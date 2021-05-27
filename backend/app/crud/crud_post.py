from app.crud.base import CRUDBase
from app.models import Post
from app.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    pass


post = CRUDPost(Post)

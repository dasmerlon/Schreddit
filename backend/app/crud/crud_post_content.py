from app.crud.crud_thing_content import CRUDThingBaseContent
from app.models import PostContent
from app.schemas import PostContentCreate, PostContentUpdate

# CRUD class for post content
post_content = CRUDThingBaseContent[PostContent, PostContentCreate, PostContentUpdate](
    PostContent
)

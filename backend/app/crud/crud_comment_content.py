from app.crud.crud_thing_content import CRUDThingBaseContent
from app.models import CommentContent
from app.schemas import CommentContentCreate, CommentContentUpdate

# CRUD class for comment content
comment_content = CRUDThingBaseContent[
    CommentContent, CommentContentCreate, CommentContentUpdate
](CommentContent)

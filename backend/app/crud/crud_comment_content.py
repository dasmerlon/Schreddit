from typing import List, Union

from pydantic import UUID4

from app.crud.crud_thing_content import CRUDThingBaseContent
from app.models import CommentContent
from app.schemas import CommentContentCreate, CommentContentUpdate


class CRUDCommentContent(
    CRUDThingBaseContent[CommentContent, CommentContentCreate, CommentContentUpdate]
):
    """Comment content class for CRUD operations"""

    def filter_by_uids(self, uids: List[Union[str, UUID4]]):
        return self.model.objects(uid__in=uids)


comment_content = CRUDCommentContent(CommentContent)

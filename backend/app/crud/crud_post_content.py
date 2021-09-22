from typing import List, Union

from mongoengine import QuerySet
from pydantic import UUID4

from app.crud.crud_thing_content import CRUDThingBaseContent
from app.models import PostContent
from app.schemas import PostContentCreate, PostContentUpdate


class CRUDPostContent(
    CRUDThingBaseContent[PostContent, PostContentCreate, PostContentUpdate]
):
    """Post content class for CRUD operations"""

    def filter_by_uids(self, uids: List[Union[str, UUID4]]) -> QuerySet:
        return self.model.objects(uid__in=uids)


post_content = CRUDPostContent(PostContent)

from typing import List, Union

from pydantic import UUID4

from app.crud.base_mongo import CRUDBaseMongo
from app.models import PostContent
from app.schemas import PostContentCreate, PostContentUpdate


class CRUDPostContent(CRUDBaseMongo[PostContent, PostContentCreate, PostContentUpdate]):
    """Post content class for CRUD operations"""

    def filter_by_uids(self, uids: List[Union[str, UUID4]]):
        return self.model.objects(uid__in=uids)


post_content = CRUDPostContent(PostContent)
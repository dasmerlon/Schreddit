from typing import List, Union

from pydantic import UUID4

from app.crud.base_mongo import (CreateSchemaType, CRUDBaseMongo, ModelType,
                                 UpdateSchemaType)
from app.models import ThingContent
from app.schemas import ThingContentCreate, ThingContentUpdate


class CRUDThingBaseContent(
    CRUDBaseMongo[ModelType, CreateSchemaType, UpdateSchemaType]
):
    """Thing content abstract base class"""

    def filter_by_uids(self, uids: List[Union[str, UUID4]]):
        return self.model.objects(uid__in=uids)


thing_content = CRUDThingBaseContent[
    ThingContent, ThingContentCreate, ThingContentUpdate
](ThingContent)

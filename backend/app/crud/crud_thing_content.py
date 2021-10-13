from typing import List, Union

from pydantic import UUID4

from app.crud.base_mongo import (CreateSchemaType, CRUDBaseMongo, ModelType,
                                 UpdateSchemaType)
from app.models import ThingContent
from app.schemas import ThingContentCreate, ThingContentUpdate


class CRUDThingBaseContent(
    CRUDBaseMongo[ModelType, CreateSchemaType, UpdateSchemaType]
):
    """CRUD base class for thing content"""

    def filter_by_uids(self, uids: List[Union[str, UUID4]]):
        """
        Filter the model type by a list of UUIDs.

        :param uids: list of UUIDs to filter by
        :return: NodeSet filtered by list of UUIDs
        """
        return self.model.objects(uid__in=uids)


thing_content = CRUDThingBaseContent[
    ThingContent, ThingContentCreate, ThingContentUpdate
](ThingContent)

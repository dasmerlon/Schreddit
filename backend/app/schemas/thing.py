from enum import IntEnum
from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

from app.schemas.thing_content import (ThingContent, ThingContentCreate,
                                       ThingContentUpdate)
from app.schemas.thing_meta import ThingMeta, ThingMetaCreate, ThingMetaUpdate

MetadataCreateType = TypeVar("MetadataCreateType", bound=ThingMetaCreate)
ContentCreateType = TypeVar("ContentCreateType", bound=ThingContentCreate)

MetadataUpdateType = TypeVar("MetadataUpdateType", bound=ThingMetaUpdate)
ContentUpdateType = TypeVar("ContentUpdateType", bound=ThingContentUpdate)

MetadataType = TypeVar("MetadataType", bound=ThingMeta)
ContentType = TypeVar("ContentType", bound=ThingContent)


class VoteOptions(IntEnum):
    upvote = 1
    novote = 0
    downvote = -1


class ThingCreate(GenericModel, Generic[MetadataCreateType, ContentCreateType]):
    metadata: MetadataCreateType
    content: ContentCreateType


class ThingUpdate(GenericModel, Generic[MetadataUpdateType, ContentUpdateType]):
    metadata: Optional[MetadataUpdateType] = None
    content: Optional[ContentUpdateType] = None


class Thing(GenericModel, Generic[MetadataType, ContentType]):
    metadata: MetadataType
    content: ContentType

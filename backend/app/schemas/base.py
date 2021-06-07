from typing import Any, Optional

from neomodel import StructuredNode
from pydantic import UUID4, BaseModel
from pydantic.utils import GetterDict

from app.models import Post


class Pagination(BaseModel):
    after: Optional[UUID4] = None
    before: Optional[UUID4] = None
    limit: int


class NeoGetterDict(GetterDict):
    """
    This class makes sure that the Pydantic from_orm mode
    only uses the properties of a StructuredNode to
    populate the model.
    """

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self._obj, StructuredNode):
            if key in self._obj.__properties__:
                return getattr(self._obj, key, default)
        else:
            return super().get(key, default)


class PostGetterDict(GetterDict):
    """
    Correctly transform the Post neomodel to the Post schema
    """

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self._obj, Post):
            if key in self._obj.__properties__:
                return getattr(self._obj, key, default)
            elif key == "author":
                return (
                    self._obj.author.single() if self._obj.author is not None else None
                )
        else:
            return super().get(key, default)

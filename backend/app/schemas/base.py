from typing import Any, Optional

from neomodel import StructuredNode
from pydantic import BaseModel
from pydantic.utils import GetterDict

from app.models import Post, Subreddit


class Pagination(BaseModel):
    prev: Optional[str] = None
    next: Optional[str] = None


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
                return self._obj.author.single() if self._obj.author else None
            elif key == "subreddit":
                return self._obj.subreddit.single() if self._obj.subreddit else None
        else:
            return super().get(key, default)


class SubredditGetterDict(GetterDict):
    """
    Correctly transform the Subreddit neomodel to the Subreddit schema
    """

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self._obj, Subreddit):
            if key in self._obj.__properties__:
                return getattr(self._obj, key, default)
            elif key == "admin":
                return self._obj.admin.single() if self._obj.admin else None
        else:
            return super().get(key, default)

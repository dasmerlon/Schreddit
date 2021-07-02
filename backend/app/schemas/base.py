from typing import Any, Optional

from neomodel import StructuredNode
from pydantic import BaseModel
from pydantic.utils import GetterDict

from app.models import CommentMeta, PostMeta, Subreddit


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
        if isinstance(self._obj, PostMeta):
            if key in self._obj.__properties__:
                return getattr(self._obj, key, default)
            elif key == "author" and hasattr(self._obj, "author"):
                return self._obj.author.single()
            elif key == "subreddit" and hasattr(self._obj, "subreddit"):
                return self._obj.subreddit.single()
        else:
            return super().get(key, default)


class CommentGetterDict(GetterDict):
    """
    Correctly transform the Comment neomodel to the Comment schema
    """

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self._obj, CommentMeta):
            if key in self._obj.__properties__:
                return getattr(self._obj, key, default)
            elif key == "author":
                return self._obj.author.single() if self._obj.author else None
            elif key == "parent":
                return self._obj.parent.single().uid if self._obj.parent else None
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
            elif key == "admin" and hasattr(self._obj, "admin"):
                return self._obj.admin.single()
        else:
            return super().get(key, default)

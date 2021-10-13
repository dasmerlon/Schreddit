from enum import Enum, auto
from typing import Any, Optional

from neomodel import StructuredNode
from pydantic import BaseModel
from pydantic.utils import GetterDict

from app.models import CommentMeta, PostMeta, Subreddit, ThingMeta


class Pagination(BaseModel):
    prev: Optional[str] = None
    next: Optional[str] = None


class CursorDirection(Enum):
    """
    Enum for the cursor direction.

    Using an ``after`` cursor returns all resources after the cursor, using a
    ``before`` cursor returns all resources before the cursor
    """

    after = auto()
    before = auto()


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


class ThingGetterDict(GetterDict):
    """
    Correctly transform the ``Thing`` neomodel to the ``Thing`` schema:

    - it maps the ``author`` field of the schema to the ``username`` field of the author
    - it maps the ``count`` field of the schema to the vote count, which counts the
      ``UPVOTED_BY`` and ``DOWNVOTED_BY`` relationships and computes the difference
    - it maps every other field to the property with the same name of the model
    """

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self._obj, ThingMeta):
            if key in self._obj.__properties__:
                return getattr(self._obj, key, default)
            elif key == "author" and hasattr(self._obj, "author"):
                author = self._obj.author.single()
                if author:
                    return author.username
            elif (
                key == "count"
                and hasattr(self._obj, "upvotes")
                and hasattr(self._obj, "downvotes")
            ):
                return len(self._obj.upvotes) - len(self._obj.downvotes)
        else:
            return super().get(key, default)


class PostGetterDict(ThingGetterDict):
    """
    Correctly transform the ``Post`` neomodel to the ``Post`` schema:

    - it maps the ``sr`` field of the schema to the ``sr`` field of the subreddit
      the post was posted in
    - it maps every other field according to ``ThingGetterDict``
    """

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self._obj, PostMeta):
            if key == "sr" and hasattr(self._obj, "subreddit"):
                subreddit = self._obj.subreddit.single()
                if subreddit:
                    return subreddit.sr
            else:
                return super().get(key, default)


class CommentGetterDict(ThingGetterDict):
    """
    Correctly transform the ``Comment`` neomodel to the ``Comment`` schema:

    - it maps the ``parent`` field of the schema to the ``uid`` of the parent thing
    - it maps every other field according to ``ThingGetterDict``
    """

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self._obj, CommentMeta):
            if key == "parent":
                parent = self._obj.parent.single()
                if parent:
                    return parent.uid
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

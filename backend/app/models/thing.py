from mongoengine import Document, StringField, UUIDField
from neomodel import (DateTimeProperty, RelationshipFrom, RelationshipTo,
                      StructuredNode, UniqueIdProperty, cardinality)

from app.models.relationships import Downvote, Upvote


class ThingMeta(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

    # Relationships
    author = RelationshipTo(
        ".user.User", "AUTHORED_BY", cardinality=cardinality.ZeroOrOne
    )
    children = RelationshipFrom(".comment.CommentMeta", "PARENT")
    downvotes = RelationshipTo(".user.User", "DOWNVOTED_BY", model=Downvote)
    upvotes = RelationshipTo(".user.User", "UPVOTED_BY", model=Upvote)


class ThingContent(Document):
    uid = UUIDField(required=True, unique=True)
    text = StringField()

    meta = {"allow_inheritance": True}

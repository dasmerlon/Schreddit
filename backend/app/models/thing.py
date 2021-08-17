from mongoengine import Document, StringField, UUIDField
from neomodel import (DateTimeProperty, RelationshipFrom, RelationshipTo,
                      StructuredNode, UniqueIdProperty, cardinality)


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


class ThingContent(Document):
    uid = UUIDField(required=True, unique=True)
    text = StringField()

    meta = {"allow_inheritance": True}

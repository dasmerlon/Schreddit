from neomodel import (DateTimeProperty, RelationshipFrom, RelationshipTo,
                      StructuredNode, UniqueIdProperty, cardinality)


class Thing(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

    # Relationships
    author = RelationshipTo(
        ".user.User", "AUTHORED_BY", cardinality=cardinality.ZeroOrOne
    )
    child = RelationshipFrom(".comment_meta.CommentMeta", "PARENT")

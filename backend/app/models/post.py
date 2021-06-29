from neomodel import (BooleanProperty, DateTimeProperty, RelationshipTo,
                      StringProperty, StructuredNode, UniqueIdProperty,
                      cardinality)


# Nodes
class Post(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    nsfw = BooleanProperty()
    spoiler = BooleanProperty()
    type = StringProperty()

    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

    # Relationships
    author = RelationshipTo(
        ".user.User", "AUTHORED_BY", cardinality=cardinality.ZeroOrOne
    )
    subreddit = RelationshipTo(
        ".subreddit.Subreddit", "POSTED_IN", cardinality=cardinality.One
    )

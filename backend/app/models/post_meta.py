from neomodel import (BooleanProperty, RelationshipTo, StringProperty,
                      cardinality)

from app.models.base import Thing


# Nodes
class PostMeta(Thing):
    # Properties
    nsfw = BooleanProperty()
    spoiler = BooleanProperty()
    type = StringProperty()

    # Relationships
    subreddit = RelationshipTo(
        ".subreddit.Subreddit", "POSTED_IN", cardinality=cardinality.One
    )

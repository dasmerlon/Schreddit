from neomodel import (BooleanProperty, DateTimeProperty, RelationshipTo,
                      StringProperty, StructuredNode, UniqueIdProperty,
                      cardinality)

from app.core.config import settings

# Relationships

# Nodes
class Post(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    nsfw = BooleanProperty()
    spoiler = BooleanProperty()
    text = StringProperty()
    title = StringProperty(max_length=settings.MAX_TITLE_LENGTH)
    type = StringProperty()
    url = StringProperty()

    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

    # Relationships
    author = RelationshipTo(".user.User", "AUTHORED_BY", cardinality=cardinality.One)
    # TODO: uncomment when subreddit logic is implemented
    # subreddit = RelationshipTo('.subreddit.Subreddit', 'POSTED_IN', cardinality=One)

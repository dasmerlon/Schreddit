from neomodel import (DateTimeProperty, RelationshipFrom, RelationshipTo,
                      StringProperty, StructuredNode, UniqueIdProperty,
                      cardinality)

from app.core.config import settings


# Nodes
class Subreddit(StructuredNode):
    # Properties
    description = StringProperty()
    # over_18 = BooleanProperty(default=False)
    # public_description = StringProperty()
    # spoilers_enable = BooleanProperty(default=False)
    sr = StringProperty(unique_index=True)
    # submit_link_label = StringProperty(max_length=60)
    # submit_text = StringProperty()
    # submit_text_label = StringProperty(max_length=60)
    title = StringProperty(max_length=settings.MAX_TITLE_LENGTH)
    type = StringProperty()
    uid = UniqueIdProperty()
    # welcome_message_enabled = BooleanProperty()
    # welcome_message_text = StringProperty()

    created_at = DateTimeProperty(default_now=True)

    # Relationships
    admin = RelationshipTo(".user.User", "CREATED_BY", cardinality=cardinality.One)
    post = RelationshipFrom(".post.Post", "POSTED_IN")

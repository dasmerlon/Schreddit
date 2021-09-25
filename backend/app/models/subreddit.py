from neomodel import (DateTimeProperty, RelationshipFrom, RelationshipTo,
                      StringProperty, StructuredNode, UniqueIdProperty,
                      cardinality)

from app.core.config import settings
from app.models.relationships import Subscription


# Nodes
class Subreddit(StructuredNode):
    # Properties
    description = StringProperty(max_length=settings.MAX_DESCRIPTION_LENGTH)
    # over_18 = BooleanProperty(default=False)
    # public_description = StringProperty()
    # spoilers_enable = BooleanProperty(default=False)
    sr = StringProperty(unique_index=True, max_length=settings.MAX_SR_LENGTH)
    title = StringProperty(max_length=settings.MAX_TITLE_LENGTH)
    type = StringProperty()
    uid = UniqueIdProperty()
    # welcome_message_enabled = BooleanProperty()
    # welcome_message_text = StringProperty()

    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

    # Relationships
    admin = RelationshipTo(".user.User", "CREATED_BY", cardinality=cardinality.One)
    post = RelationshipFrom(".post.PostMeta", "POSTED_IN")
    subscriber = RelationshipFrom(".user.User", "SUBSCRIBED_TO", model=Subscription)

from mongoengine import StringField, URLField
from neomodel import (BooleanProperty, RelationshipTo, StringProperty,
                      cardinality)

from app.core.config import settings
from app.models.thing import ThingContent, ThingMeta


class PostContent(ThingContent):
    title = StringField(max_length=settings.MAX_TITLE_LENGTH)
    url = URLField()


class PostMeta(ThingMeta):
    # Properties
    nsfw = BooleanProperty()
    spoiler = BooleanProperty()
    type = StringProperty()

    # Relationships
    subreddit = RelationshipTo(
        ".subreddit.Subreddit", "POSTED_IN", cardinality=cardinality.One
    )

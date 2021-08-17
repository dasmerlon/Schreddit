from neomodel import RelationshipTo, cardinality

from app.models.thing import ThingContent, ThingMeta


class CommentContent(ThingContent):
    pass


class CommentMeta(ThingMeta):
    # Relationships
    parent = RelationshipTo(".thing.ThingMeta", "PARENT", cardinality=cardinality.One)

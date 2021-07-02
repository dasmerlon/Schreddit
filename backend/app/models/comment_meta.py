from neomodel import RelationshipTo, cardinality

from app.models.base import Thing


# Nodes
class CommentMeta(Thing):
    # Relationships
    parent = RelationshipTo(".base.Thing", "PARENT", cardinality=cardinality.One)

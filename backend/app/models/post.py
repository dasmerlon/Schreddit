from neomodel import StructuredNode, StructuredRel, RelationshipTo
from neomodel import (DateTimeProperty,
                      EmailProperty,
                      StringProperty,
                      UniqueIdProperty)


# Relationships


# Nodes
class Post(StructuredNode):
    # Properties
    uid = UniqueIdProperty()

from neomodel import (DateTimeProperty, RelationshipTo, StructuredNode,
                      UniqueIdProperty, cardinality)


class Thing(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

    # Relationships
    author = RelationshipTo(
        ".user.User", "AUTHORED_BY", cardinality=cardinality.ZeroOrOne
    )

from neomodel import StructuredNode, StructuredRel, RelationshipTo
from neomodel import (DateTimeProperty,
                      EmailProperty,
                      StringProperty,
                      UniqueIdProperty)


# Relationships
class Friendship(StructuredRel):
    since = DateTimeProperty(default_now=True)


# Nodes
class User(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    email = EmailProperty(unique_index=True)
    username = StringProperty(unique_index=True)
    hashed_password = StringProperty()

    # Relationships
    friend = RelationshipTo('User', 'FRIENDS_WITH', model=Friendship)

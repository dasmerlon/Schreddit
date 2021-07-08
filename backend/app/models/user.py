from neomodel import (DateTimeProperty, EmailProperty, RelationshipFrom,
                      RelationshipTo, StringProperty, StructuredNode,
                      StructuredRel, UniqueIdProperty)


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
    friend = RelationshipTo("User", "FRIENDS_WITH", model=Friendship)
    post_author = RelationshipFrom(".post.Post", "AUTHORED_BY")

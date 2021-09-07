from neomodel import (EmailProperty, RelationshipFrom, RelationshipTo,
                      StringProperty, StructuredNode, UniqueIdProperty)

from app.models.relationships import Downvote, Friendship, Upvote


class User(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    email = EmailProperty(unique_index=True)
    username = StringProperty(unique_index=True)
    hashed_password = StringProperty()

    # Relationships
    friend = RelationshipTo("User", "FRIENDS_WITH", model=Friendship)
    author = RelationshipFrom(".post.PostMeta", "AUTHORED_BY")
    downvotes = RelationshipFrom(".thing.ThingMeta", "DOWNVOTED_BY", model=Downvote)
    upvotes = RelationshipFrom(".thing.ThingMeta", "UPVOTED_BY", model=Upvote)

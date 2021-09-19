import math

from mongoengine import Document, StringField, UUIDField
from neomodel import (DateTimeProperty, RelationshipFrom, RelationshipTo,
                      StructuredNode, UniqueIdProperty, cardinality)

from app.models.relationships import Downvote, Upvote


class ThingMeta(StructuredNode):
    # Properties
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

    # Relationships
    author = RelationshipTo(
        ".user.User", "AUTHORED_BY", cardinality=cardinality.ZeroOrOne
    )
    children = RelationshipFrom(".comment.CommentMeta", "PARENT")
    downvotes = RelationshipTo(".user.User", "DOWNVOTED_BY", model=Downvote)
    upvotes = RelationshipTo(".user.User", "UPVOTED_BY", model=Upvote)

    def vote_count(self):
        """
        Get the vote count for a thing.
        It is defined as ``upvotes - downvotes``.

        :return: vote count
        """
        return len(self.upvotes) - len(self.downvotes)

    def hot_score(self):
        """
        Get the hot ranking score for a thing.

        :return: the hot score
        """
        #  CAUTION: IF MODIFYING THIS, ALSO MODIFY ALGORITHM IN cypher.py
        score = len(self.upvotes) - len(self.downvotes)
        order = math.log10(max(abs(score), 1))
        if score > 0:
            sign = 1
        elif score < 0:
            sign = -1
        else:
            sign = 0
        seconds = self.created_at.timestamp() - 1134028003
        return round(sign * order + seconds / 45000, 7)


class ThingContent(Document):
    uid = UUIDField(required=True, unique=True)
    text = StringField()

    meta = {"allow_inheritance": True}

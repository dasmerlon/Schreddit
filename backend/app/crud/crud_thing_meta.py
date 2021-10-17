from neomodel import db

from app.crud.base_neo import (CreateSchemaType, CRUDBaseNeo, ModelType,
                               UpdateSchemaType)
from app.models import ThingMeta, User
from app.schemas import ThingMetaCreate, ThingMetaUpdate, VoteOptions


class CRUDThingBaseMeta(CRUDBaseNeo[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD base class for thing metadata"""

    @db.read_transaction
    def get_author(self, db_obj: ThingMeta) -> User:
        """
        Get the author of a thing.

        :param db_obj: the thing whose author should be returned
        :return: the author of the thing
        """
        return db_obj.author.single()

    @db.write_transaction
    def set_author(self, db_obj: ThingMeta, author: User) -> None:
        """
        Set the author of a thing.

        :param db_obj: the thing whose author should be set
        :param author: the new author of the thing
        """
        db_obj.author.connect(author)

    @db.read_transaction
    def get_vote_count(self, db_obj: ThingMeta) -> int:
        """
        Return the vote count of a thing.
        The vote count is defined as ``upvotes-downvotes``

        :param db_obj: the thing whose vote count should be returned
        :return: the vote count of the thing
        """
        return len(db_obj.upvotes) - len(db_obj.downvotes)

    @db.read_transaction
    def get_vote_state(self, db_obj: ThingMeta, user: User) -> VoteOptions:
        """
        Return the vote state of a thing for a user.

        :param db_obj: the thing whose vote state should be returned
        :param user: the user for whom the vote state should be returned
        :return: the vote state of the thing
        """
        if db_obj.downvotes.get_or_none(uid=user.uid):
            return VoteOptions.downvote
        elif db_obj.upvotes.get_or_none(uid=user.uid):
            return VoteOptions.upvote
        else:
            return VoteOptions.novote

    @db.write_transaction
    def downvote(self, db_obj: ThingMeta, user: User, state: VoteOptions) -> None:
        """
        Downvote a thing for a user.

        :param db_obj: the thing that should be downvoted
        :param user: the user that downvoted the thing
        :param state: vote state of the thing
        """
        # if already downvoted, don't do anything
        if state == VoteOptions.downvote:
            return

        # if previously upvoted, remove upvote
        if state == VoteOptions.upvote:
            db_obj.upvotes.disconnect(user)

        db_obj.downvotes.connect(user)

    @db.write_transaction
    def upvote(self, db_obj: ThingMeta, user: User, state: VoteOptions) -> None:
        """
        Upvote a thing for a user.

        :param db_obj: the thing that should be upvoted
        :param user: the user that upvoted the thing
        :param state: vote state of the thing
        """
        # if already upvoted, don't do anything
        if state == VoteOptions.upvote:
            return

        # if previously downvoted, remove downvote
        if state == VoteOptions.downvote:
            db_obj.downvotes.disconnect(user)

        db_obj.upvotes.connect(user)

    @db.write_transaction
    def remove_vote(self, db_obj: ThingMeta, user: User, state: VoteOptions) -> None:
        """
        Remove the vote of a thing for a user.

        :param db_obj: the thing whose vote should be removed
        :param user: the user that unvoted the thing
        :param state: vote state of the thing
        """
        if state == VoteOptions.upvote:
            db_obj.upvotes.disconnect(user)
        elif state == VoteOptions.downvote:
            db_obj.downvotes.disconnect(user)


thing_meta = CRUDThingBaseMeta[ThingMeta, ThingMetaCreate, ThingMetaUpdate](ThingMeta)

from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import ThingNotFoundException

router = APIRouter()


@router.put(
    "/{uid}/{dir}",
    name="Vote on a thing",
)
def vote(
    uid: UUID4,
    dir: schemas.VoteOptions,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Vote a thing up or down or remove a vote.

    - `uid` : UUID of the thing to vote
    - `dir` : direction of the vote,
    `1` for upvotes, `-1` for downvotes and `0` for unvoting
    """
    thing_meta = crud.thing_meta.get(uid)
    if not thing_meta:
        raise ThingNotFoundException

    state = crud.thing_meta.get_vote_state(thing_meta, current_user)

    if state == dir:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    if dir == schemas.VoteOptions.upvote:
        crud.thing_meta.upvote(thing_meta, current_user, state)
    elif dir == schemas.VoteOptions.downvote:
        crud.thing_meta.downvote(thing_meta, current_user, state)
    elif dir == schemas.VoteOptions.novote:
        crud.thing_meta.remove_vote(thing_meta, current_user, state)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{uid}/state",
    name="Get vote state on a thing",
    response_model=schemas.VoteOptions,
    status_code=status.HTTP_200_OK,
)
def get_vote_state(
    uid: UUID4, current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get current vote state of a thing.

    :param uid: UUID of the post
    :return current vote -- `1` for upvoted, `-1` for downvoted and `0` for unvoted
    """
    thing_meta = crud.thing_meta.get(uid)
    if not thing_meta:
        raise ThingNotFoundException

    return crud.thing_meta.get_vote_state(thing_meta, current_user)


@router.get(
    "/{uid}/count", name="Get vote count on a thing", status_code=status.HTTP_200_OK
)
def get_vote_count(uid: UUID4):
    """
    Get current vote count of a thing.

    :param uid: UUID of the post
    :return current vote count
    """
    thing_meta = crud.thing_meta.get(uid)
    if not thing_meta:
        raise ThingNotFoundException

    return crud.thing_meta.get_vote_count(thing_meta)

from app import crud
from app.models import PostContent, PostMeta, User


def test_upvote_post(
    post_self_in_db_other_user: (PostMeta, PostContent), test_user_in_db: User
) -> None:
    metadata = post_self_in_db_other_user[0]
    state = crud.thing_meta.get_vote_state(metadata, test_user_in_db)
    crud.thing_meta.upvote(metadata, test_user_in_db, state)
    assert crud.thing_meta.get_vote_state(metadata, test_user_in_db) == 1
    assert crud.thing_meta.get_vote_count(metadata) == 1


def test_downvote_post(
    post_self_in_db_other_user: (PostMeta, PostContent), test_user_in_db: User
) -> None:
    metadata = post_self_in_db_other_user[0]
    state = crud.thing_meta.get_vote_state(metadata, test_user_in_db)
    crud.thing_meta.downvote(metadata, test_user_in_db, state)
    assert crud.thing_meta.get_vote_state(metadata, test_user_in_db) == -1
    assert crud.thing_meta.get_vote_count(metadata) == -1


def test_remove_vote_from_post(
    post_self_in_db_upvoted: (PostMeta, PostContent), test_user_in_db: User
) -> None:
    metadata = post_self_in_db_upvoted[0]
    state = crud.thing_meta.get_vote_state(metadata, test_user_in_db)
    crud.thing_meta.remove_vote(metadata, test_user_in_db, state)
    assert crud.thing_meta.get_vote_state(metadata, test_user_in_db) == 0
    assert crud.thing_meta.get_vote_count(metadata) == 0

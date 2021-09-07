from typing import List

from app import crud
from app.models import Subreddit, User
from app.tests.utils.fake_schemas import SubredditSchemas


def test_get_subreddit(subreddit_in_db: Subreddit) -> None:
    sr = subreddit_in_db
    subreddit = crud.subreddit.get_by_sr(sr.sr)
    assert subreddit
    assert subreddit == sr


def test_get_subreddit_fail(subreddit_in_db: Subreddit) -> None:
    subreddit = crud.subreddit.get_by_sr("test2")
    assert subreddit is None


def test_create_subreddit(test_user_in_db: User, remove_subreddits: List) -> None:
    obj_in = SubredditSchemas.get_create(type="public")
    subreddit = crud.subreddit.create(obj_in)
    crud.subreddit.set_admin(subreddit, test_user_in_db)
    admin = subreddit.admin.single()
    remove_subreddits.append(subreddit.uid)
    assert admin.email == test_user_in_db.email
    assert admin.username == test_user_in_db.username
    assert obj_in.sr == subreddit.sr
    assert obj_in.title == subreddit.title
    assert obj_in.type == subreddit.type


def test_update_subreddit(subreddit_in_db: Subreddit) -> None:
    obj_in = SubredditSchemas.get_update(type="public")
    subreddit = subreddit_in_db
    crud.subreddit.update(subreddit, obj_in)
    updated_subreddit = crud.subreddit.get(subreddit.uid)
    assert updated_subreddit.uid == subreddit.uid
    for key in obj_in.dict():
        assert getattr(updated_subreddit, key) == getattr(obj_in, key)

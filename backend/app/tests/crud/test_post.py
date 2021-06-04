from app import crud
from app.models import Post, User
from app.schemas.post import PostCreate, PostUpdate


def test_create_post(
    fake_random_user_in_db: User, fake_schema_post_create_link: PostCreate, remove_post
) -> None:
    post = crud.post.create(fake_schema_post_create_link, fake_random_user_in_db)
    author = post.author.single()
    remove_post(post.uid)
    for key in fake_schema_post_create_link.dict():
        if key != "sr":
            assert getattr(post, key) == getattr(fake_schema_post_create_link, key)
    assert author.email == fake_random_user_in_db.email
    assert author.username == fake_random_user_in_db.username
    # TODO: assert subreddit


def test_update_post(
    fake_link_post_in_db: Post,
    fake_schema_post_update_link: PostUpdate,
) -> None:
    fake_schema_post_update_link.uid = fake_link_post_in_db.uid
    updated_post = crud.post.update(fake_link_post_in_db, fake_schema_post_update_link)
    for key in fake_schema_post_update_link.dict():
        assert getattr(updated_post, key) == getattr(fake_schema_post_update_link, key)

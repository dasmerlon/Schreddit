from app import crud
from app.schemas.post import PostCreate, PostType


def test_create_post(database) -> None:
    nsfw = True
    spoiler = False
    sr = "subreddit"
    title = "This is a link"
    type = PostType.link
    url = "https://www.google.com/"

    post_create = PostCreate(
        nsfw=nsfw, spoiler=spoiler, sr=sr, title=title, type=type, url=url
    )
    post = crud.post.create(post_create)
    for key in post_create.dict():
        if key != "sr":
            assert getattr(post, key) == getattr(post_create, key)
    # TODO: assert subreddit

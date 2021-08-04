from typing import List, Union

from faker import Faker
from neomodel import clear_neo4j_database, db

from app import crud, models, schemas
from app.db.init_db import init_neo4j, init_mongodb


fake = Faker()


def init_dbs():
    """Initialize databases."""
    init_neo4j()
    init_mongodb()


def create_users(count: int) -> List[models.User]:
    """
    Create random users.

    :param count: number of users to create
    :return: list of users
    """
    users = []
    for _ in range(count):
        schema = schemas.UserCreate(
            email=fake.unique.ascii_safe_email(),
            username=fake.unique.user_name(),
            password=fake.password(),
        )
        users.append(crud.user.create(schema))
    print(f"Created {count} fake users.")
    return users


def create_subreddits(count, users: List[models.User]) -> List[models.Subreddit]:
    """
    Create random subreddits.

    :param count: number of subreddits to create
    :param users: list of users that can be subreddit admins
    :return: list of subreddits
    """
    subreddits = []
    for _ in range(count):
        schema = schemas.SubredditCreate(
            sr=fake.unique.word(),
            title=" ".join(fake.words()),
            type=fake.random_element(schemas.SubredditType),
        )
        sr = crud.subreddit.create(schema)
        crud.subreddit.set_admin(sr, fake.random_element(users))
        subreddits.append(sr)
    print(f"Created {count} fake subreddits.")
    return subreddits


def create_posts(
    count: int, users: List[models.User], subreddits: List[models.Subreddit]
) -> List[models.PostMeta]:
    """
    Create random posts.

    :param count: number of posts to create
    :param users: list of users that can create a post
    :param subreddits: list of subreddits that can contain posts
    :return: list of posts
    """
    posts = []
    for _ in range(count):
        type = fake.random_element(schemas.PostType)
        metadata = schemas.PostMetaCreate(
            nsfw=fake.boolean(),
            spoiler=fake.boolean(),
            sr=fake.random_element([sr.sr for sr in subreddits]),
            type=type,
        )
        content = schemas.PostContentCreate(
            text=fake.paragraph() if type == schemas.PostType.self else None,
            title=fake.sentence(),
            url=fake.url() if type != schemas.PostType.self else None,
        )
        post = crud.post_meta.create(metadata)
        crud.post_content.create(post.uid, content)
        crud.post_meta.set_author(post, fake.random_element(users))
        crud.post_meta.set_subreddit(post, fake.random_element(subreddits))
        posts.append(post)
    print(f"Created {count} fake posts.")
    return posts


def create_comments(
    count: int,
    users: List[models.User],
    parents: Union[List[models.PostMeta], List[models.CommentMeta]],
) -> List[models.CommentMeta]:
    """
    Create random comments.

    :param count: number of comments to create
    :param users: list of users that can create a comment
    :param parents: list of posts or comments that can be parents of the comments
    :return: list of comments
    """
    comments = []
    for _ in range(count):
        schema = schemas.CommentCreate(text=fake.paragraph())
        comment = crud.comment_meta.create(None)
        crud.comment_content.create(comment.uid, schema)
        crud.comment_meta.set_author(comment, fake.random_element(users))
        crud.comment_meta.set_parent(comment, fake.random_element(parents))
        comments.append(comment)
    print(f"Created {count} fake comments.")
    return comments


def fill(
    *,
    users: int = 10,
    subreddits: int = 10,
    posts: int = 10,
    comments: int = 10,
    comments_depth_level: int = 3,
):
    """
    Fill the databases with random fake data.

    :param users: number of users to create
    :param subreddits: number of subreddits to create
    :param posts: number of posts to create
    :param comments: number of comments to create per level
    :param comments_max_depth: maximum depth of comment tree
    """
    init_dbs()
    fake_users = create_users(users)
    fake_subreddits = create_subreddits(subreddits, fake_users)
    fake_posts = create_posts(posts, fake_users, fake_subreddits)
    fake_comments = create_comments(comments, fake_users, fake_posts)
    for _ in range(comments_depth_level - 1):
        fake_comments = create_comments(comments, fake_users, fake_comments)


def clear():
    """Clear the databases."""
    i = input("Are you sure you want to clear the databases? (y/N)")
    if i == "y":
        init_dbs()
        clear_neo4j_database(db)
        models.PostContent.drop_collection()
        models.CommentContent.drop_collection()
        print("Cleared the databases.")
    else:
        print("Not removing anything")

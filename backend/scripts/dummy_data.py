#!/usr/bin/env python3

import argparse
import requests
from typing import List, Union

from faker import Faker
from neomodel import clear_neo4j_database, db

from app import crud, models, schemas
from app.core.config import settings
from app.db.init_db import init_neo4j, init_mongodb


fake = Faker()


def init_dbs():
    """Initialize databases."""
    init_neo4j()
    init_mongodb()


def create_username():
    while True:
        username = fake.unique.user_name()
        if (
                settings.MIN_USERNAME_LENGTH
                <= len(username)
                <= settings.MAX_USERNAME_LENGTH
        ):
            break
    return username


def create_sr():
    while True:
        sr = fake.unique.word()
        if settings.MIN_SR_LENGTH <= len(sr) <= settings.MAX_SR_LENGTH:
            break
    return sr


def create_users(count: int) -> List[models.User]:
    """
    Create random users and one fixed dummy user.

    :param count: number of users to create
    :return: list of users
    """
    users = []

    # create test user
    dummy_schema = schemas.UserCreate(
        email="dummy@data.com",
        username="dummy",
        password="data",
    )
    users.append(crud.user.create(dummy_schema))

    # create random users
    for _ in range(count - 1):
        schema = schemas.UserCreate(
            email=fake.unique.ascii_safe_email(),
            username=create_username(),
            password=fake.password(),
        )
        users.append(crud.user.create(schema))
    print(f"Created the dummy user and {count - 1} fake users.")
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
            description=" ".join(fake.words()),
            sr=create_sr(),
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
        post_type = fake.random_element(schemas.PostType)
        metadata = schemas.PostMetaCreate(
            nsfw=fake.boolean(),
            spoiler=fake.boolean(),
            sr=fake.random_element([sr.sr for sr in subreddits]),
            type=post_type,
        )

        # set content according to post type
        text = None
        url = None
        if post_type == schemas.PostType.image:
            url = requests.get("https://picsum.photos/600/300").url
        elif post_type == schemas.PostType.video:
            url = (
                "https://test-videos.co.uk/"
                "vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4"
            )
        elif post_type == schemas.PostType.link:
            url = fake.url()
        elif post_type == schemas.PostType.self:
            text = fake.paragraph()
        content = schemas.PostContentCreate(
            text=text,
            title=fake.sentence(),
            url=url
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
        metadata = schemas.CommentMetaCreate()
        content = schemas.CommentContentCreate(text=fake.paragraph())
        comment = crud.comment_meta.create(metadata)
        crud.comment_content.create(comment.uid, content)
        crud.comment_meta.set_author(comment, fake.random_element(users))
        crud.comment_meta.set_parent(comment, fake.random_element(parents))
        comments.append(comment)
    print(f"Created {count} fake comments.")
    return comments


def create_votes(
        count: int, users: List[models.User], things: List[models.ThingMeta]
) -> None:
    """

    :param count: number of votes per user
    :param users: list of users for whom votes are created
    :param things: list of things that can be voted
    :return:
    """
    for user in users:
        for _ in range(count):
            vote = fake.random_element([-1, 1])
            index = fake.unique.random_int(0, len(things) - 1)
            state = crud.thing_meta.get_vote_state(things[index], user)
            if vote == -1:
                crud.thing_meta.downvote(things[index], user, state)
            elif vote == 1:
                crud.thing_meta.upvote(things[index], user, state)
        fake.unique.clear()
    print(f"Created {count} fake votes per user.")


def create_subscriptions(
        count: int, users: List[models.User], subreddits: List[models.Subreddit]
) -> None:
    """
    Create random subreddit subscriptions for users
    :param count: number of subscriptions per user
    :param users: list of users for whom subscriptions are created
    :param subreddits: list of subreddits that are subscribed by the users
    """
    for user in users:
        for _ in range(count):
            index = fake.unique.random_int(0, len(subreddits) - 1)
            crud.subreddit.set_subscription(subreddits[index], user)
        fake.unique.clear()
    print(f"Created {count} fake subscriptions per user.")


def fill(
        users: int,
        subreddits: int,
        posts: int,
        comments: int,
        depth: int,
        votes: int,
        subscriptions: int,
) -> None:
    """
    Fill the databases with random fake data.

    :param users: number of users to create
    :param subreddits: number of subreddits to create
    :param posts: number of posts to create
    :param comments: number of comments to create per level
    :param depth: maximum depth of comment tree
    :param votes: number of votes per user
    :param subscriptions: number of subscriptions per user
    """
    init_dbs()
    fake_users = create_users(users)
    fake_subreddits = create_subreddits(subreddits, fake_users)
    things = []  # will hold all posts and comments
    fake_posts = create_posts(posts, fake_users, fake_subreddits)
    things.extend(fake_posts)
    fake_comments = create_comments(comments, fake_users, fake_posts)
    things.extend(fake_comments)
    for _ in range(depth - 1):
        fake_comments = create_comments(comments, fake_users, fake_comments)
        things.extend(fake_comments)
    create_votes(votes, fake_users, things)
    create_subscriptions(subscriptions, fake_users, fake_subreddits)


def clear():
    """Clear the databases."""
    i = input("Are you sure you want to clear the databases? (y/N) ")
    if i == "y":
        init_dbs()
        clear_neo4j_database(db)
        models.PostContent.drop_collection()
        models.CommentContent.drop_collection()
        print("Cleared the databases.")
    else:
        print("Not removing anything")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fill the databases with dummy data or clear all data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "action", choices=["fill", "clear"], help="either fill or clear the databases"
    )
    parser.add_argument(
        "-u", "--users", default=10, help="number of users to create", type=int
    )
    parser.add_argument(
        "-s",
        "--subreddits",
        default=10,
        help="number of subreddits to create",
        type=int,
    )
    parser.add_argument(
        "-p", "--posts", default=20, help="number of posts to create", type=int
    )
    parser.add_argument(
        "-c",
        "--comments",
        default=50,
        help="number of comments to create for each depth level",
        type=int,
    )
    parser.add_argument(
        "-d", "--depth", default=3, help="maximum depth of the comment tree", type=int
    )
    parser.add_argument(
        "-v",
        "--votes",
        default=50,
        help="number of votes to create for each user",
        type=int,
    )
    parser.add_argument(
        "-a",
        "--subscriptions",
        default=5,
        help="number of subscriptions to create for each user",
        type=int,
    )

    args = parser.parse_args()
    if args.action == "fill":
        fill(
            args.users,
            args.subreddits,
            args.posts,
            args.comments,
            args.depth,
            args.votes,
            args.subscriptions
        )
    elif args.action == "clear":
        clear()

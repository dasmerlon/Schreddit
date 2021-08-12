from app import schemas
from app.core.config import settings


class UserSchemas:
    """User schemas"""

    @staticmethod
    def get_create_test_user():
        return schemas.UserCreate(
            email=settings.TEST_USER_EMAIL,
            username=settings.TEST_USER_USERNAME,
            password=settings.TEST_USER_PASSWORD,
        )

    @staticmethod
    def get_create_other_user():
        return schemas.UserCreate(
            email="other@user.com",
            username="other",
            password="password",
        )

    @staticmethod
    def get_update():
        return schemas.UserUpdate(
            email="new@mail.com",
            password="newpassword",
        )


class PostSchemas:
    """Post schemas"""

    @staticmethod
    def get_create(*, type: str = "link", valid: bool = True):
        metadata = schemas.PostMetaCreate(
            nsfw=True if type == "link" else False,
            spoiler=False if type == "link" else True,
            sr="",
            type=type,
        )
        content = schemas.PostContentCreate(
            text="A text." if type != "link" or not valid else None,
            title="A Title",
            url="https://www.google.com/" if type == "link" or not valid else None,
        )
        return schemas.PostCreate(metadata=metadata, content=content)

    @staticmethod
    def get_update(*, type: str = "link", valid: bool = True):
        metadata = schemas.PostMetaUpdate(
            nsfw=False if type == "link" else True,
            spoiler=True if type == "link" else False,
        )
        content = schemas.PostContentUpdate(
            text="An updated text." if type != "link" or not valid else None,
            title="An Updated Title",
            url="https://www.update.com/" if type == "link" or not valid else None,
        )
        return schemas.PostUpdate(metadata=metadata, content=content)


class CommentSchemas:
    @staticmethod
    def get_create():
        return schemas.CommentCreate(text="A comment.")

    @staticmethod
    def get_update():
        return schemas.CommentUpdate(text="An updated comment.")


class SubredditSchemas:
    """Subreddit schemas"""

    @staticmethod
    def get_create(*, type: str = "public"):
        return schemas.SubredditCreate(
            description="A subreddit description.",
            sr="test",
            title="A Subreddit Title",
            type=type,
        )

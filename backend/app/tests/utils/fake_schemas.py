from app import schemas
from app.core.config import settings


class UserSchemas:
    """User schemas"""

    @staticmethod
    def get_create():
        return schemas.UserCreate(
            email=settings.TEST_USER_EMAIL,
            username=settings.TEST_USER_USERNAME,
            password=settings.TEST_USER_PASSWORD,
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
        return schemas.PostCreate(
            nsfw=True if type == "link" else False,
            spoiler=False if type == "link" else True,
            sr="testsr",
            text="A text." if type != "link" or not valid else None,
            title="A Title",
            url="https://www.google.com/" if type == "link" or not valid else None,
            type=type,
        )

    @staticmethod
    def get_update(*, type: str = "link", valid: bool = True):
        return schemas.PostUpdate(
            nsfw=False if type == "link" else True,
            spoiler=True if type == "link" else False,
            text="An updated text." if type != "link" or not valid else None,
            title="An Updated Title",
            url="https://www.update.com/" if type == "link" or not valid else None,
        )

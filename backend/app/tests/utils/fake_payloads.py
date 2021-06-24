from app.core.config import settings


class UserPayloads:
    """User payloads"""

    @staticmethod
    def get_create():
        return {
            "email": settings.TEST_USER_EMAIL,
            "username": settings.TEST_USER_USERNAME,
            "password": settings.TEST_USER_PASSWORD,
        }

    @staticmethod
    def get_update():
        return {
            "email": "new@mail.com",
            "password": "newpassword",
        }

    @staticmethod
    def get_auth():
        return {
            "username": settings.TEST_USER_EMAIL,
            "password": settings.TEST_USER_PASSWORD,
        }


class PostPayloads:
    """Post payloads"""

    @staticmethod
    def get_create(*, type: str = "link", valid: bool = True):
        return {
            "nsfw": True if type == "link" else False,
            "spoiler": False if type == "link" else True,
            "sr": "testsr",
            "text": "A text." if type != "link" or not valid else None,
            "title": "A Title",
            "url": "https://www.google.com/" if type == "link" or not valid else None,
            "type": type,
        }

    @staticmethod
    def get_update(*, type: str = "link", valid: bool = True):
        return {
            "nsfw": False if type == "link" else True,
            "spoiler": True if type == "link" else False,
            "text": "An updated text." if type != "link" or not valid else None,
            "title": "An Updated Title",
            "url": "https://www.update.com/" if type == "link" or not valid else None,
        }

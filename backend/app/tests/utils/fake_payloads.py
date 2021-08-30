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
    def get_auth_by_email():
        return {
            "username": settings.TEST_USER_EMAIL,
            "password": settings.TEST_USER_PASSWORD,
        }

    @staticmethod
    def get_auth_by_username():
        return {
            "username": settings.TEST_USER_USERNAME,
            "password": settings.TEST_USER_PASSWORD,
        }


class PostPayloads:
    """Post payloads"""

    @staticmethod
    def get_create(*, type: str = "link", valid: bool = True):
        return {
            "metadata": {
                "nsfw": True if type == "link" else False,
                "spoiler": False if type == "link" else True,
                "type": type,
            },
            "content": {
                "text": "A text." if type != "link" or not valid else None,
                "title": "A Title",
                "url": "https://www.google.com/"
                if type == "link" or not valid
                else None,
            },
        }

    @staticmethod
    def get_update(*, type: str = "link", valid: bool = True):
        return {
            "metadata": {
                "nsfw": False if type == "link" else True,
                "spoiler": True if type == "link" else False,
            },
            "content": {
                "text": "An updated text." if type != "link" or not valid else None,
                "title": "An Updated Title",
                "url": "https://www.update.com/"
                if type == "link" or not valid
                else None,
            },
        }


class CommentPayloads:
    """Comment payloads"""

    @staticmethod
    def get_create():
        return {"metadata": {}, "content": {"text": "A comment."}}

    @staticmethod
    def get_update():
        return {"content": {"text": "An updated comment."}}


class SubredditPayloads:
    """Subreddit payloads"""

    @staticmethod
    def get_create(*, type: str = "public"):
        return {
            "description": "A subreddit description.",
            "title": "A subreddit title",
            "type": type,
            "sr": "test",
        }

    @staticmethod
    def get_update(*, type: str = "public"):
        return {
            "description": "An updated subreddit description.",
            "title": "An updated subreddit title",
            "type": type,
        }

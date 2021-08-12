from mongoengine import Document, StringField, URLField, UUIDField

from app.core.config import settings


class PostContent(Document):
    uid = UUIDField(required=True, unique=True)
    text = StringField()
    title = StringField(max_length=settings.MAX_TITLE_LENGTH)
    url = URLField()

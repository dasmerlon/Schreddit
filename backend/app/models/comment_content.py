from mongoengine import Document, StringField, UUIDField


class CommentContent(Document):
    uid = UUIDField(required=True, unique=True)
    text = StringField()

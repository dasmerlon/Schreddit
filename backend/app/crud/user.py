from neomodel import db
from app.models import User
from app.schemas import UserCreate


@db.read_transaction
def get_by_email(user: UserCreate):
    return User.nodes.get_or_none(email=user.email)


@db.read_transaction
def get_by_username(user: UserCreate):
    return User.nodes.get_or_none(username=user.username)


@db.write_transaction
def create(user: UserCreate):
    hashed_password = user.password  # TODO: hash password
    user_model = User(email=user.email,
                      username=user.username,
                      hashed_password=hashed_password)
    user_model.save()
    return user_model

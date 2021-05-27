from app import crud, schemas
from app.core.config import settings


def override_get_current_user():
    return crud.user.get_by_email(settings.TEST_USER_EMAIL)


def create_test_user() -> schemas.User:
    email = settings.TEST_USER_EMAIL
    username = settings.TEST_USER_USERNAME
    password = settings.TEST_USER_PASSWORD
    user_in = schemas.UserCreate(email=email, username=username, password=password)
    user = crud.user.create(user_in)
    return user

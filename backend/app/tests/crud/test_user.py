from typing import List

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models import User
from app.tests.utils.fake_schemas import UserSchemas


def test_create_user(remove_users: List) -> None:
    obj_in = UserSchemas.get_create_test_user()
    user = crud.user.create(obj_in)
    remove_users.append(user.uid)
    assert user
    assert user.email == obj_in.email
    assert user.username == obj_in.username
    assert hasattr(user, "hashed_password")


def test_authenticate_by_email(test_user_in_db: User) -> None:
    user = crud.user.authenticate_by_email(
        email=settings.TEST_USER_EMAIL, password=settings.TEST_USER_PASSWORD
    )
    assert user
    assert user.email == settings.TEST_USER_EMAIL
    assert user.username == settings.TEST_USER_USERNAME


def test_authentication_by_email_fail() -> None:
    email = "noauth@example.com"
    password = "1"
    user = crud.user.authenticate_by_email(email, password)
    assert user is None


def test_authenticate_by_username(test_user_in_db: User) -> None:
    user = crud.user.authenticate_by_username(
        username=settings.TEST_USER_USERNAME, password=settings.TEST_USER_PASSWORD
    )
    assert user
    assert user.email == settings.TEST_USER_EMAIL
    assert user.username == settings.TEST_USER_USERNAME


def test_authentication_by_username_fail() -> None:
    username = "noauth"
    password = "1"
    user = crud.user.authenticate_by_username(username, password)
    assert user is None


def test_get_user_by_email(test_user_in_db: User) -> None:
    user = crud.user.get_by_email(test_user_in_db.email)
    assert user
    assert user.email == test_user_in_db.email
    assert user.username == test_user_in_db.username


def test_update_user_schema(test_user_in_db: User) -> None:
    obj_in = UserSchemas.get_update()
    crud.user.update(test_user_in_db, obj_in)
    updated_user = crud.user.get(test_user_in_db.uid)
    assert updated_user
    assert test_user_in_db.username == updated_user.username
    assert obj_in.email == updated_user.email
    assert verify_password(obj_in.password, updated_user.hashed_password)


def test_update_user_schema_dict(test_user_in_db: User) -> None:
    obj_in = UserSchemas.get_update()
    crud.user.update(test_user_in_db, obj_in.dict())
    updated_user = crud.user.get(test_user_in_db.uid)
    assert updated_user
    assert test_user_in_db.username == updated_user.username
    assert obj_in.email == updated_user.email
    assert verify_password(obj_in.password, updated_user.hashed_password)

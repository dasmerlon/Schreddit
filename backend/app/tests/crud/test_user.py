from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models import User
from app.schemas import UserCreate, UserUpdate


def test_create_user(fake_schema_test_user_create: UserCreate, remove_user) -> None:
    user = crud.user.create(fake_schema_test_user_create)
    remove_user(user.uid)
    assert user
    assert user.email == fake_schema_test_user_create.email
    assert user.username == fake_schema_test_user_create.username
    assert hasattr(user, "hashed_password")


def test_authenticate_user(fake_test_user_in_db: User) -> None:
    user = crud.user.authenticate(
        email=settings.TEST_USER_EMAIL, password=settings.TEST_USER_PASSWORD
    )
    assert user
    assert user.email == settings.TEST_USER_EMAIL
    assert user.username == settings.TEST_USER_USERNAME


def test_authentication_fail() -> None:
    email = "noauth@example.com"
    password = "1"
    user = crud.user.authenticate(email, password)
    assert user is None


def test_get_user_by_email(fake_random_user_in_db: User) -> None:
    user = crud.user.get_by_email(fake_random_user_in_db.email)
    assert user
    assert user.email == fake_random_user_in_db.email
    assert user.username == fake_random_user_in_db.username


def test_update_user(fake_random_user_in_db: User) -> None:
    new_password = "ithinkthisisbetter"
    user_in_update = UserUpdate(password=new_password)
    crud.user.update(fake_random_user_in_db, user_in_update)
    updated_user = crud.user.get(fake_random_user_in_db.uid)
    assert updated_user
    assert fake_random_user_in_db.email == updated_user.email
    assert fake_random_user_in_db.username == updated_user.username
    assert verify_password(new_password, updated_user.hashed_password)

    new_password = "thisisdefinitelybetter"
    user_in_update = UserUpdate(password=new_password)
    obj_in_data = jsonable_encoder(user_in_update)
    crud.user.update(fake_random_user_in_db, obj_in_data)
    updated_user = crud.user.get(fake_random_user_in_db.uid)
    assert updated_user
    assert fake_random_user_in_db.email == updated_user.email
    assert fake_random_user_in_db.username == updated_user.username
    assert verify_password(new_password, updated_user.hashed_password)

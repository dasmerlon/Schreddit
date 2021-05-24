from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate


def test_create_user() -> None:
    email = "create@example.com"
    username = "create"
    password = "password"
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.user.create(obj_in=user_in)
    assert user.email == email
    assert user.username == username
    assert hasattr(user, "hashed_password")


def test_authenticate_user() -> None:
    email = "authenticate@example.com"
    username = "authenticate"
    password = "password"
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.user.create(obj_in=user_in)
    authenticated_user = crud.user.authenticate(email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email
    assert user.username == authenticated_user.username


def test_not_authenticate_user() -> None:
    email = "noauth@example.com"
    password = "1"
    user = crud.user.authenticate(email=email, password=password)
    assert user is None


def test_get_user() -> None:
    email = "getme@example.com"
    username = "getme"
    password = "password"
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.user.create(obj_in=user_in)

    created_user = crud.user.get(user.uid)
    assert created_user
    assert user.email == created_user.email
    assert user.username == created_user.username
    assert jsonable_encoder(user) == jsonable_encoder(created_user)


def test_update_user() -> None:
    email = "unsure@example.com"
    username = "unsure"
    password = "pleasechangeme"
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.user.create(obj_in=user_in)

    new_password = "ithinkthisisbetter"
    user_in_update = UserUpdate(password=new_password)
    crud.user.update(db_obj=user, obj_in=user_in_update)
    updated_user = crud.user.get(user.uid)
    assert updated_user
    assert user.email == updated_user.email
    assert user.username == updated_user.username
    assert verify_password(new_password, updated_user.hashed_password)

    new_password = "thisisdefinitelybetter"
    user_in_update = UserUpdate(password=new_password)
    print(user_in_update)
    obj_in_data = jsonable_encoder(user_in_update)
    crud.user.update(db_obj=user, obj_in=obj_in_data)
    updated_user = crud.user.get(user.uid)
    assert updated_user
    assert user.email == updated_user.email
    assert user.username == updated_user.username
    assert verify_password(new_password, updated_user.hashed_password)

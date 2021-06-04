import pytest
from faker import Faker

from app.core.config import settings
from app.schemas import PostCreate, PostType, PostUpdate, UserCreate

"""
Fake User schemas
"""


@pytest.fixture
def fake_schema_user_create(faker: Faker):
    return UserCreate(
        email=faker.email(), username=faker.user_name(), password=faker.password()
    )


@pytest.fixture
def fake_schema_test_user_create():
    return UserCreate(
        email=settings.TEST_USER_EMAIL,
        username=settings.TEST_USER_USERNAME,
        password=settings.TEST_USER_PASSWORD,
    )


"""
Fake Post schemas
"""


@pytest.fixture
def fake_schema_post_create_link(faker: Faker):
    return PostCreate(
        nsfw=faker.pybool(),
        spoiler=faker.pybool(),
        sr=faker.word(),
        title=faker.sentence(),
        url=faker.url(),
        type=PostType.link,
    )


@pytest.fixture
def fake_schema_post_update_link(faker: Faker, faker_seed: int):
    return PostUpdate(
        uid="",  # must be updated in the actual test
        nsfw=faker.pybool(),
        spoiler=faker.pybool(),
        title=faker.sentence(),
        url=faker.url(),
    )


@pytest.fixture
def fake_schema_post_create_self(faker: Faker):
    return PostCreate(
        nsfw=faker.pybool(),
        spoiler=faker.pybool(),
        sr=faker.word(),
        text=faker.paragraph(),
        title=faker.sentence(),
        type=PostType.self,
    )


@pytest.fixture
def fake_schema_post_update_self(faker: Faker, faker_seed: int):
    return PostUpdate(
        uid="",  # must be updated in the actual test
        nsfw=faker.pybool(),
        spoiler=faker.pybool(),
        text=faker.paragraph(),
        title=faker.sentence(),
    )

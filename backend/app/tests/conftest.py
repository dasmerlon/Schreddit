from typing import Generator

import pytest
from fastapi.testclient import TestClient
from neomodel import config

from app.api.deps import get_current_user
from app.core.config import settings
from app.main import app
from app.tests.utils.user import override_get_current_user

pytest_plugins = ["app.tests.fixtures.fake_schemas", "app.tests.fixtures.fake_db"]


@pytest.fixture(autouse=True, scope="session")
def database():
    config.DATABASE_URL = settings.NEO4J_TEST_BOLT_URL


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def faker_seed():
    return 1


@pytest.fixture
def fake_test_user_auth(fake_test_user_in_db):
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield fake_test_user_in_db
    app.dependency_overrides = {}

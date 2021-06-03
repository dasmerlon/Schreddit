from typing import Generator

import pytest
from fastapi.testclient import TestClient
from neomodel import clear_neo4j_database, config, db

from app.api.deps import get_current_user
from app.core.config import settings
from app.main import app
from app.models import User
from app.tests.utils.user import create_test_user, override_get_current_user


@pytest.fixture(scope="session")
def init_database():
    config.DATABASE_URL = settings.NEO4J_TEST_BOLT_URL


@pytest.fixture(autouse=True, scope="function")
def database(init_database):
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


@pytest.fixture(scope="function")
def fake_user() -> User:
    return create_test_user()


@pytest.fixture
def fake_auth(fake_user):
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield fake_user
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

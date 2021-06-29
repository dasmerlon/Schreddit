from typing import Generator

import pytest
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
from neomodel import config

from app import crud
from app.api.deps import get_current_user
from app.core.config import settings
from app.main import app

pytest_plugins = ["app.tests.fixtures.fixtures_db"]


@pytest.fixture(autouse=True, scope="session")
def database():
    config.DATABASE_URL = settings.NEO4J_TEST_BOLT_URL


@pytest.fixture(autouse=True, scope="session")
def mongodb():
    connect(host=settings.MONGODB_TEST_URI)
    yield
    disconnect()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def fake_auth(test_user_in_db):
    app.dependency_overrides[get_current_user] = lambda: crud.user.get_by_email(
        settings.TEST_USER_EMAIL
    )
    yield test_user_in_db
    app.dependency_overrides = {}

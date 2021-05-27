from typing import Generator

import pytest
from fastapi.testclient import TestClient
from neomodel import clear_neo4j_database, config, db

from app.core.config import settings
from app.main import app


@pytest.fixture(scope="session")
def database():
    config.DATABASE_URL = settings.NEO4J_TEST_BOLT_URL
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

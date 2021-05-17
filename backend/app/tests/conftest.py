from typing import Generator

import pytest
from app.config import settings
from fastapi.testclient import TestClient
from app.main import app
from neomodel import config, clear_neo4j_database, db


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
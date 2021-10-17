from mongoengine import connect
from neomodel import config

from app.core.config import settings


def init_neo4j():
    """Initialize Neo4j with the correct URL."""
    config.DATABASE_URL = settings.NEO4J_BOLT_URL


def init_mongodb():
    """Initialize MongoDB with the correct URL."""
    connect(host=settings.MONGODB_URI)

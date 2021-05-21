from neomodel import config

from app.config import settings


def init_neo4j():
    config.DATABASE_URL = settings.NEO4J_BOLT_URL

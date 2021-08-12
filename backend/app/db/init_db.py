from mongoengine import connect
from neomodel import config

from app.core.config import settings


def init_neo4j():
    config.DATABASE_URL = settings.NEO4J_BOLT_URL


def init_mongodb():
    connect(host=settings.MONGODB_URI)

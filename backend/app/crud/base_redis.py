# base_redis.py
from typing import Optional

from redis import Redis

from app.core.config import settings


class CRUDBaseRedis:
    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
        )

    def get(self, key: str) -> Optional[bytes]:
        return self.redis.get(key)

    def set(
        self, key: str, value: str, ttl: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    ):
        self.redis.set(key, value, ex=ttl)


# crud_session.py
session = CRUDBaseRedis()

from pathlib import Path
from typing import Set

from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    NEO4J_BOLT_URL: str
    NEO4J_TEST_BOLT_URL: str
    MONGODB_URI: str
    MONGODB_TEST_URI: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    SUB_PREFIX: str = "uid:"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REDIS_DSN: RedisDsn = "redis://localhost:6379/0"

    MAX_TITLE_LENGTH = 300
    MAX_USERNAME_LENGTH = 20

    TEST_USER_USERNAME: str
    TEST_USER_EMAIL: str
    TEST_USER_PASSWORD: str

    FRONTEND_ORIGINS: Set[str] = {
        "http://localhost:3000",
        "https://kind-sea-014761903.azurestaticapps.net",
    }

    class Config:
        case_sensitive = True
        env_file = Path(__file__).parent.parent.absolute() / Path(".env")


settings = Settings()

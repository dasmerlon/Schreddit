from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    NEO4J_BOLT_URL: str
    NEO4J_TEST_BOLT_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    SUB_PREFIX: str = "uid:"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MAX_TITLE_LENGTH = 300

    TEST_USER_USERNAME: str
    TEST_USER_EMAIL: str
    TEST_USER_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = Path(__file__).parent.parent.absolute() / Path(".env")


settings = Settings()

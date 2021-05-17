from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    NEO4J_BOLT_URL: str
    NEO4J_TEST_BOLT_URL: str

    class Config:
        case_sensitive = True
        env_file = Path(__file__).parent.absolute() / Path(".env")


settings = Settings()
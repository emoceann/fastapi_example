import sys

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from dotenv import find_dotenv
from functools import lru_cache


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    TEST_HOST: str
    TEST_DB: str

    JWT_ENCRYPT_ALGORITHM: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=find_dotenv("dev.env"))

    @model_validator(mode="after")
    def build_test_database_url(cls, data):
        if "pytest" in sys.modules:
            data.POSTGRES_DB = data.TEST_DB
            data.POSTGRES_HOST = data.TEST_HOST
        return data


@lru_cache
def get_settings() -> Settings:
    return Settings()

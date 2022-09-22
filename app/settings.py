from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MONGO_DB_HOST: str
    MONGO_DB_PORT: int

    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"


settings = Settings()


@lru_cache
def get_client():
    return AsyncIOMotorClient(host=settings.MONGO_DB_HOST, port=settings.MONGO_DB_PORT)

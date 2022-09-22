from functools import lru_cache, partial

from pydantic import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient


@lru_cache
def get_client():
    return AsyncIOMotorClient(host="127.0.0.1", port=27017)


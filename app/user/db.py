import json
from typing import Dict, Any

import pymongo.errors
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from abc import abstractmethod

from pymongo.errors import InvalidOperation

from app.user import schemas
from app.user.factories import PyObjectId
from app.user.models import User
from app.user.schemas import UserEditRequest


class UserIsNone(Exception):
    pass

async def get_user(client: AsyncIOMotorClient, filter: Dict[str, Any]) -> User:
    collection = client.database.users
    db_user = await collection.find_one(filter)
    if db_user is None:
        raise UserIsNone
    return User(**db_user)


async def create_user(client: AsyncIOMotorClient, payload: User):
    collection = client.database.users
    usr_dict = payload.dict(by_alias=True)
    await collection.insert_one(usr_dict)
    new_user = await get_user(client, filter={"_id": usr_dict["_id"]})
    return new_user


async def edit_user(client: AsyncIOMotorClient, payload: UserEditRequest):
    collection = client.database.users
    filter_by_id = {"_id": payload.id}
    await collection.update_one(filter_by_id, {"$set": {**payload.dict()}})
    updated_user = await get_user(client, filter=filter_by_id)
    return updated_user

async def delete_user(client: AsyncIOMotorClient, filter: Dict[str, Any]):
    collection = client.database.users
    await collection.delete_one(filter=filter)








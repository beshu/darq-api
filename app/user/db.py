from typing import Dict, Any

from motor.motor_asyncio import AsyncIOMotorClient

from app.user.models import User
from app.user.schemas import UserEditRequest


class UserIsNone(Exception):
    pass


async def get_user(client: AsyncIOMotorClient, filter: Dict[str, Any]) -> User:
    db_user = await client.database.users.find_one(filter=filter)
    if db_user is None:
        raise UserIsNone
    return User(**db_user)


async def create_user(client: AsyncIOMotorClient, payload: User):
    usr_dict = payload.dict(by_alias=True)
    await client.database.users.insert_one(usr_dict)
    new_user = await get_user(client, filter={"_id": usr_dict["_id"]})
    return new_user


async def edit_user(client: AsyncIOMotorClient, payload: UserEditRequest):
    filter_by_id = {"_id": payload.id}
    await client.database.users.update_one(filter_by_id, {"$set": {**payload.dict()}})
    updated_user = await get_user(client, filter=filter_by_id)
    return updated_user


async def delete_user(client: AsyncIOMotorClient, filter: Dict[str, Any]):
    await client.database.users.delete_one(filter=filter)

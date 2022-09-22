import motor.motor_asyncio
from bson import ObjectId
from fastapi import Depends, Security, APIRouter, HTTPException
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from starlette import status

from app.auth.credentials import hash_password
from app.auth.dependencies import have_permissions
from app.user import schemas
from app.user.db import UserIsNone
from app.user.factories import PyObjectId
from app.user.models import User
from app.settings import get_client
from app.user import db
from app.user.schemas import UserEditRequest

r = APIRouter(prefix="/users")


@r.patch("/edit", dependencies=[Security(have_permissions, scopes=["admin"])])
async def edit_user(payload: UserEditRequest,
                    client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_client)):

    updated_user = await db.edit_user(client, payload)
    return {"message": "ok", "user": updated_user}


@r.get("/{user_id}", response_model=User)
async def get_user(user_id: str, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_client)):
    try:
        user = await db.get_user(client=client, filter={"_id": PyObjectId(user_id)})
        return user
    except UserIsNone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no such user with requested id")
    except PyMongoError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@r.post("/create", response_model=User)
async def create_user(payload: schemas.UserCreateRequest, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_client)):
    try:
        user = User(**payload.dict()) if payload.permissions else User(**payload.dict(exclude={"permissions"}))
        user.hashed_pass = hash_password(payload.password)
        return await db.create_user(client, user)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@r.delete("/delete/{user_id}")
async def delete_user(user_id: str, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_client)):
    try:
        await db.delete_user(client, filter={"_id": PyObjectId(user_id)})
        return {"message": "ok", "deleted": f"{user_id}"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

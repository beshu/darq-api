from datetime import datetime

import motor.motor_asyncio
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from app.auth import credentials
from app.settings import get_client
from app.user import db
from app.user.db import UserIsNone
from app.user.schemas import UserEditRequest

r = APIRouter(prefix="/auth")


@r.post("/token")
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_client),
):
    username, password = form_data.username, form_data.password
    try:
        db_user = await db.get_user(client, filter={"first_name": username})
        if form_data.scopes == [role.value for role in db_user.role]:
            if credentials.password_matches_hash(
                password, db_user.hashed_pass.get_secret_value().encode("utf-8") # noqa
            ):
                token = credentials.make_jwt_token(
                    claims={"sub": form_data.username, "scopes": form_data.scopes}
                )
                db_user.last_login = datetime.utcnow()
                edit_request = UserEditRequest(**db_user.dict())
                await db.edit_user(client, payload=edit_request)
                return {"access_token": token, "token_type": "bearer"}
    except UserIsNone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unable to get token. "
        "Either credentials are incorrect "
        "or requested scopes are not allowed for this user",
    )

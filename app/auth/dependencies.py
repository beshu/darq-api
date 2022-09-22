from datetime import datetime
from typing import List, Optional, Tuple, Dict

import motor.motor_asyncio
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import BaseModel, Field, ValidationError

from app.auth.config import SECRET_KEY, ALGORITHM
from app.auth.enums import Role
from app.settings import get_client
from app.user import db
from app.user.db import UserIsNone
from app.user.factories import PyObjectId
from app.user.models import User

auth_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        Role.admin.value: "admin rights",
        Role.dev.value: "dev rights",
        Role.simple_mortal.value: "simple mortal rights (can't do anything)"
    },
)


class TokenClaims(BaseModel):
    username: str = Field(alias="sub")
    expire: Optional[datetime] = Field(alias="exp", default=None)
    not_before: Optional[datetime] = Field(alias="nbf", default=None)
    issuer: Optional[datetime] = Field(alias="iss", default=None)
    issued_at: Optional[datetime] = Field(alias="iat", default=None)
    audience: Optional[List[str]] = Field(alias="aud", default=[])


class Token(BaseModel):
    claims: TokenClaims
    scopes: Optional[str] = None


async def token_user_exists(sc: SecurityScopes,
                            token: str = Depends(auth_scheme),
                            client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_client)
                            ) -> Dict[str, Token | User]:
    auth_header = "Bearer"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        valid_token = Token(claims=TokenClaims(**payload))
        if sc.scopes:
            valid_token.scopes = sc.scope_str
            auth_header = auth_header + f" scope={sc.scope_str}"
        user = await db.get_user(client, filter={"first_name": valid_token.claims.username})
    except (JWTError, ValidationError, UserIsNone) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Access denied: {e}",
            headers={
                "WWW-Authenticate": auth_header
            },
        )
    return {"token": valid_token, "user": user}


async def have_permissions(payload: Dict[str, Token | User] = Depends(token_user_exists)):
    user, token = payload["user"], payload["token"]
    token_scopes = token.scopes.split()
    user_scopes = [role.value for role in user.role]

    if not any(list(map(lambda scope: scope in token_scopes, user_scopes))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": f'Bearer scope="{token.scopes}"'}
        )
    return user


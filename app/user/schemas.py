from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

import app.auth.enums as auth
from app.user.factories import PyObjectId
from app.user.models import User


class UserEditRequest(BaseModel):
    id: PyObjectId
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool]
    role: Optional[List[auth.Role]]
    created_at: Optional[datetime]
    last_login: Optional[datetime]


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    password: str
    role: Optional[str]


class UserCreateResponse(User):
    class Config:
        fields = {"hashed_pass": {"exclude": True}}

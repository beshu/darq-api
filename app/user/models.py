from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, validator, Field, SecretStr

import app.auth.enums as auth
from app.user.factories import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str
    last_name: str
    hashed_pass: Optional[SecretStr]
    is_active: bool = True
    role: List[auth.Role] = Field(default=[auth.Role.simple_mortal])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        keep_untouched = (datetime,)
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }

    @validator("role", always=True, pre=True)
    def role_is_ok(cls, v) -> List[auth.Role]:
        if isinstance(v, str):
            arr = v.split()
            allowed_roles = [r.value for r in auth.Role]

            if not all(list(map(lambda r: r in allowed_roles, arr))):
                raise ValueError("Role should be admin, dev or mortal ")

            return [getattr(auth.Role, scope) for scope in arr]
        return v

    @validator("first_name", "last_name")
    def name_is_ascii(cls, v: str) -> Optional[str]:
        if not v.isascii():
            raise ValueError("Value should consist of ASCII characters only")
        return v

    @validator("first_name", "last_name")
    def name_is_not_too_long(cls, v: str) -> Optional[str]:
        if len(v) > 50:
            raise ValueError("Value is too long: only 50 characters is permitted")
        return v

    @validator("is_active")
    def is_not_active(cls, v):
        if not v:
            raise ValueError("User cannot be inactive")
        return v

    @validator("created_at")
    def date_in_future(cls, v: datetime) -> Optional[datetime]:
        if datetime.now() < v:
            raise ValueError("Date should be in past")
        return v

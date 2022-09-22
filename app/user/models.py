from datetime import datetime
from enum import Enum
from typing import Optional, Union, Type, List

import bcrypt as bcrypt
from bson import ObjectId
from pydantic import BaseModel, validator, Field, SecretStr

import app.auth.enums as auth
from app.user.factories import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str
    last_name: str
    hashed_pass: Optional[SecretStr] = Field(exclude=True)
    is_active: bool = True
    role: List[auth.Role] = Field(default=[auth.Role.simple_mortal], alias="permissions")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        keep_untouched = (datetime,)
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, SecretStr: lambda v: v.get_secret_value() if v else None}

    @validator("role", always=True, pre=True)
    def cast_to_enum(cls, v) -> List[auth.Role]:
        if isinstance(v, str):
            return [getattr(auth.Role, scope) for scope in v.split()]
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

    @validator("role", check_fields=False)
    def roles_ok(cls, v: auth.Role) -> auth.Role:
        return v  # Pydantic provides automatic validation for role's choice if Enum is presented in type hint

    @validator("is_active")
    def is_not_active(cls, v):
        if not v:
            raise ValueError("User cannot be inactive at creation")
        return v

    @validator("created_at")
    def date_in_future(cls, v: datetime) -> Optional[datetime]:
        if datetime.now() < v:
            raise ValueError("Date should be in past")
        return v

if __name__ == '__main__':
    user = User(first_name="Daniil", last_name="Sheremet", permissions=[auth.Role.admin], hashed_pass=str(bcrypt.hashpw(b"1234", bcrypt.gensalt())))
    print(user)

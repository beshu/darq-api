from pydantic import Field
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class TokenClaims(BaseModel):
    username: str = Field(alias="sub")
    expire: Optional[datetime] = Field(alias="exp", default=None)
    not_before: Optional[datetime] = Field(alias="nbf", default=None)
    issuer: Optional[datetime] = Field(alias="iss", default=None)
    issued_at: Optional[datetime] = Field(alias="iat", default=None)
    audience: Optional[List[str]] = Field(alias="aud", default=[])


class Token(BaseModel):
    claims: TokenClaims
    scopes: Optional[str]


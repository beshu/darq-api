from datetime import timedelta, datetime
from typing import Optional

import bcrypt
from jose import jwt

from app.settings import settings


def hash_password(raw_pw: str) -> bytes:
    return bcrypt.hashpw(password=raw_pw.encode("utf-8"), salt=bcrypt.gensalt())


def password_matches_hash(raw_pw: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password=raw_pw.encode("utf-8"), hashed_password=hashed)


def make_jwt_token(claims: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    claims.update({"exp": expire})
    return jwt.encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

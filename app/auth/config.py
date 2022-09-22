from fastapi.security import OAuth2PasswordBearer

from app.auth.enums import Role

SECRET_KEY = "834b3ddd895cf6e10039fdd43f3b0d1d5145de503a58819ffa16550a1d11edc7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10




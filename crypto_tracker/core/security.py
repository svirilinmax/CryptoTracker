import time

import jwt
from aiohttp import web
from passlib.hash import pbkdf2_sha256
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Потом в env закинем
JWT_SECRET = 'CHANGE_ME_SUPER_SECRET_32CHARS'
JWT_ALG = 'HS256'
JWT_EXPIRE_SEC = 60 * 60 * 24 * 7  # 7 дней
COOKIE_NAME = 'token'


# -------------Password-------------------
def make_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pbkdf2_sha256.verify(password, password_hash)


# -------------Token-------------------
def make_token(user_id: int, username: str) -> str:
    now = int(time.time())
    payload = {"sub": user_id, "username": username, "iat": now, "exp": now + JWT_EXPIRE_SEC}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG], options={"verify_sub": False})


# -------------User-------------------
async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        from crud.user import get_user_by_id
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
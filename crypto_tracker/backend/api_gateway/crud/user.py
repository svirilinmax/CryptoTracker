from backend.api_gateway.core.security import make_password_hash
from backend.api_gateway.models.database import User
from backend.api_gateway.models.schemas import UserCreateRequest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreateRequest):
    hashed_password = make_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
    )

    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        # Определяем какое поле вызвало ошибку
        if "email" in str(e.orig):
            raise HTTPException(400, "Email уже занят")
        elif "username" in str(e.orig):
            raise HTTPException(400, "Username уже занят")
        else:
            raise HTTPException(500, "Ошибка создания пользователя")

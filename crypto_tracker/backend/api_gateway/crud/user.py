from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.api_gateway.models.database import User
from backend.api_gateway.models.schemas import UserCreateRequest
from backend.api_gateway.core.security import make_password_hash

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
    db_user = User(email=user_data.email, username=user_data.username, password_hash=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
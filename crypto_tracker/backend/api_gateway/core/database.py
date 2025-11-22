from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.api_gateway.core.config import settings


DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

async def create_tables():
    """
    Создает все таблицы в базе данных
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_async_session():
    return async_session()
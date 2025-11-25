from backend.api_gateway.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# TODO: Добавьте commit/rollback для корректной работы транзакций
# При ошибке изменения не откатываются и БД остается в inconsistent state
# См. REVIEW.md секция "Критические проблемы" пункт 5
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()  # TODO: добавить
        except Exception:
            await session.rollback()  # TODO: добавить
            raise
        finally:
            await session.close()  # TODO: добавить


async def create_tables():
    """
    Создает все таблицы в базе данных
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_async_session():
    return async_session()

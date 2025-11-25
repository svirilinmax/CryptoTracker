from typing import List

from backend.api_gateway.models.database import PriceHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_price_history(
    db: AsyncSession, asset_id: int, price: float
) -> PriceHistory:
    """
    Создать запись в истории цен
    """
    price_history = PriceHistory(asset_id=asset_id, price=price)
    db.add(price_history)
    await db.commit()
    await db.refresh(price_history)
    return price_history


async def get_price_history_by_asset(
    db: AsyncSession, asset_id: int, skip: int = 0, limit: int = 50
) -> List[PriceHistory]:
    """
    Получить историю цен для актива
    """
    if limit > 1000:
        limit = 1000
    result = await db.execute(
        select(PriceHistory)
        .where(PriceHistory.asset_id == asset_id)
        .order_by(PriceHistory.recorded_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

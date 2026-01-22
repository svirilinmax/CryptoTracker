from models.database import PriceHistory
from sqlalchemy.ext.asyncio import AsyncSession


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

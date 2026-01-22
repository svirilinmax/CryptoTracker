from typing import List, Optional

from models.database import Asset
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .price_repo import create_price_history


# _______________WORKER_____________________#
async def get_all_active_assets(db: AsyncSession) -> List[Asset]:
    """
    Получить все активные валюты (для WORKER задачи)
    """
    result = await db.execute(select(Asset).where(Asset.is_active.is_(True)))
    return result.scalars().all()


async def update_asset_price(
    db: AsyncSession, asset_id: int, current_price: float
) -> Optional[Asset]:
    """
    Обновить текущую цену актива и записать в историю
    """

    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()

    if asset:
        asset.current_price = current_price
        await create_price_history(db, asset_id, current_price)
        await db.commit()
        await db.refresh(asset)

    return asset

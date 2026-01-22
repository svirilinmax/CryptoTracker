import logging
from typing import List, Optional

from fastapi import HTTPException
from models.database import Asset
from models.schemas import AssetCreateRequest, AssetUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

logger = logging.getLogger("price_delete_asset")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def get_assets_by_user(db: AsyncSession, user_id: int) -> List[Asset]:
    """
    Получает ВСЕ активы конкретного пользователя (включая и неактивные)
    """
    result = await db.execute(select(Asset).where(Asset.user_id == user_id))
    return result.scalars().all()


async def get_active_assets_by_user(db: AsyncSession, user_id: int) -> List[Asset]:
    """
    Получить только АКТИВНЫЕ активы пользователя
    """
    result = await db.execute(
        select(Asset).where(Asset.user_id == user_id, Asset.is_active.is_(True))
    )
    return result.scalars().all()


async def get_asset_by_id(
    db: AsyncSession, asset_id: int, user_id: int
) -> Optional[Asset]:
    """
    Получить ОДИН актив по ID (только активный)
    """
    result = await db.execute(
        select(Asset).where(
            Asset.id == asset_id, Asset.user_id == user_id, Asset.is_active.is_(True)
        )
    )
    return result.scalar_one_or_none()


async def create_asset(
    db: AsyncSession, asset_data: AssetCreateRequest, user_id: int
) -> Asset:
    """
    Создать новый актив
    """
    from services.price_service import get_current_price

    current_price = await get_current_price(asset_data.symbol.upper())

    db_asset = Asset(
        user_id=user_id,
        symbol=asset_data.symbol.upper(),
        min_price=asset_data.min_price,
        max_price=asset_data.max_price,
        current_price=current_price,
        is_active=True,
    )
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    if current_price is not None:
        from repositories.price_history import create_price_history

        await create_price_history(db, db_asset.id, current_price)
    return db_asset


async def restore_asset_by_id(
    db: AsyncSession, asset_id: int, user_id: int
) -> Optional[Asset]:
    """
    Восстановить неактивный актив
    """
    # Ищем ЛЮБОЙ актив (включая неактивные)
    result = await db.execute(
        select(Asset).where(Asset.id == asset_id, Asset.user_id == user_id)
    )
    asset = result.scalar_one_or_none()

    if asset:
        asset.is_active = True
        await db.commit()
        await db.refresh(asset)
    return asset


async def update_asset(
    db: AsyncSession, asset_id: int, asset_data: AssetUpdateRequest, user_id: int
) -> Optional[Asset]:
    """
    Обновить существующий актив
    """
    from services.price_service import get_current_price

    asset = await get_asset_by_id(db, asset_id, user_id)
    if not asset:
        return None

    if asset_data.symbol and asset_data.symbol != asset.symbol:
        current_price = await get_current_price(asset_data.symbol.upper())
        asset.current_price = current_price

    update_data = asset_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)

    await db.commit()
    await db.refresh(asset)
    return asset


async def delete_asset(db: AsyncSession, asset_id: int, user_id: int) -> bool:
    """
    Удалить актив из отслеживаемых
    """
    asset = await get_asset_by_id(db, asset_id, user_id)
    if not asset:
        logger.warning(
            f"Delete attempt for non-existent or "
            f"unauthorized asset_id={asset_id} by user_id={user_id}"
        )
        return False

    if asset.user_id != user_id:
        logger.error(
            f"SECURITY: User {user_id} attempted "
            f"to delete asset {asset_id} owned by {asset.user_id}"
        )
        raise HTTPException(403, "Forbidden")

    asset.is_active = False
    await db.commit()
    logger.info(f"Asset {asset_id} deleted by user {user_id}")
    return True

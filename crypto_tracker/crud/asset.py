from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models.database import Asset
from models.schemas import AssetCreateRequest, AssetUpdateRequest


async def get_assets_by_user(db: AsyncSession, user_id: int) -> List[Asset]:
    """
    Получает ВСЕ активы конкретного пользователя (включая и неактивные)

    Args:
        db (AsyncSession): Сессия базы данных
        user_id (int): ID пользователя

    Returns:
        List[Asset]: Список всех активов этого пользователя
    """
    result = await db.execute(select(Asset).where(Asset.user_id == user_id))
    return result.scalars().all()


async def get_active_assets_by_user(db: AsyncSession, user_id: int) -> List[Asset]:
    """
    Получить только АКТИВНЫЕ активы пользователя
    """
    result = await db.execute(select(Asset).where(
        Asset.user_id == user_id,
        Asset.is_active == True
    ))
    return result.scalars().all()


async def get_asset_by_id(db: AsyncSession, asset_id: int, user_id: int) -> Optional[Asset]:
    """
    Получить ОДИН актив по ID (только активный)

    Args:
        db (AsyncSession): Сессия базы данных
        asset_id (int): ID актива
        user_id (int): ID пользователя (для проверки принадлежности)

    Returns:
        Optional[Asset]: Найденный актив или None если не найден или не принадлежит пользователю
    """
    result = await db.execute(select(Asset).where(
        Asset.id == asset_id,
        Asset.user_id == user_id,
        Asset.is_active == True
    ))
    return result.scalar_one_or_none()


async def create_asset(db: AsyncSession, asset_data: AssetCreateRequest, user_id: int) -> Asset:
    """
    Создать новый актив

    Args:
        db (AsyncSession): Сессия базы данных
        asset_data (AssetCreateRequest): Данные для создания актива
        user_id (int): ID пользователя-владельца

    Returns:
        Asset: Созданный актив
    """
    db_asset = Asset(
        user_id=user_id,
        symbol=asset_data.symbol.upper(),
        min_price=asset_data.min_price,
        max_price=asset_data.max_price,
        is_active=True
    )
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    return db_asset


async def restore_asset_by_id(db: AsyncSession, asset_id: int, user_id: int) -> Optional[Asset]:
    """
    Восстановить неактивный актив
    """
    # Ищем ЛЮБОЙ актив (включая неактивные)
    result = await db.execute(select(Asset).where(Asset.id == asset_id,Asset.user_id == user_id))
    asset = result.scalar_one_or_none()

    if asset:
        asset.is_active = True
        await db.commit()
        await db.refresh(asset)
    return asset


async def update_asset(db: AsyncSession,
                       asset_id: int,
                       asset_data: AssetUpdateRequest,
                       user_id: int) -> Optional[Asset]:
    """
       Обновить существующий актив
       Args:
           db: Сессия базы данных
           asset_id: ID актива для обновления
           asset_data: Новые данные для обновления
           user_id: ID пользователя (для проверки принадлежности)
       Returns:
           Asset | None: Обновленный актив или None если не найден
       """
    asset = await get_asset_by_id(db, asset_id, user_id)
    if not asset:
        return None

    update_data = asset_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)

    await db.commit()
    await db.refresh(asset)
    return asset


async def delete_asset(db: AsyncSession, asset_id: int, user_id: int) -> bool:
    """
        Удалить актив из отслеживаемых
        Args:
            db (AsyncSession): Сессия базы данных
            asset_id (int): ID актива для удаления
            user_id (int): ID пользователя (для проверки принадлежности)
        Returns:
            bool: True если удаление успешно, False если актив не найден
        """

    asset = await get_asset_by_id(db, asset_id, user_id)
    if not asset:
        return False

    asset.is_active = False
    await db.commit()
    return True


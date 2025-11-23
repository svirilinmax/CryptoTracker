from typing import List

from backend.api_gateway.core.database import get_db
from backend.api_gateway.core.security import get_current_user
from backend.api_gateway.crud.asset import (
    create_asset,
    delete_asset,
    get_active_assets_by_user,
    get_asset_by_id,
    get_assets_by_user,
    restore_asset_by_id,
    update_asset,
)
from backend.api_gateway.crud.price_history import get_price_history_by_asset
from backend.api_gateway.models.database import User
from backend.api_gateway.models.schemas import (
    AssetCreateRequest,
    AssetResponse,
    AssetUpdateRequest,
    PriceHistory,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[AssetResponse])
async def get_my_assets(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Получить все активные валюты текущего пользователя"""
    assets = await get_active_assets_by_user(db, current_user.id)
    return assets


@router.get("/all", response_model=List[AssetResponse])
async def get_all_my_assets(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Получить все валюты текущего пользователя (включая неактивные)"""
    assets = await get_assets_by_user(db, current_user.id)
    return assets


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Получить конкретный актив по ID"""
    asset = await get_asset_by_id(db, asset_id, current_user.id)

    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.post("/", response_model=AssetResponse)
async def create_new_asset(
    asset_data: AssetCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Создать новый актив для отслеживания"""
    asset = await create_asset(db, asset_data, current_user.id)
    return asset


@router.post("/{asset_id}/restore", response_model=AssetResponse)
async def restore_asset(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Восстановить неактивный актив"""
    asset = await restore_asset_by_id(db, asset_id, current_user.id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_existing_asset(
    asset_id: int,
    asset_data: AssetUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Обновить данные актива"""
    asset = await update_asset(db, asset_id, asset_data, current_user.id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.delete("/{asset_id}")
async def delete_existing_asset(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Удалить валюту"""
    result = await delete_asset(db, asset_id, current_user.id)
    if not result:
        raise HTTPException(404, "Asset not found")
    return {"message": "Asset deleted successfully"}


@router.get("/{asset_id}/history", response_model=List[PriceHistory])
async def get_asset_price_history(
    asset_id: int,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получить историю цен для конкретного актива
    """
    asset = await get_asset_by_id(db, asset_id, current_user.id)
    if not asset:
        raise HTTPException(404, "Asset not found")

    history = await get_price_history_by_asset(db, asset_id, limit)
    return history


@router.post("/{asset_id}/refresh")
async def refresh_asset_price(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Мгновенное обновление цены актива"""
    from backend.api_gateway.crud.asset import update_asset_price
    from backend.api_gateway.services.price_service import get_current_price

    asset = await get_asset_by_id(db, asset_id, current_user.id)
    if not asset:
        raise HTTPException(404, "Asset not found")

    current_price = await get_current_price(asset.symbol)
    if current_price is not None:
        await update_asset_price(db, asset_id, current_price)
        return {"status": "updated", "price": current_price, "symbol": asset.symbol}
    else:
        return {"status": "failed", "message": "Could not fetch current price"}

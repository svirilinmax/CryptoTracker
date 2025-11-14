from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from watchfiles import awatch

from core.database import get_db
from core.security import get_current_user
from models.database import User, Asset
from models.schemas import AssetResponse, AssetCreateRequest, AssetUpdateRequest
from crud.asset import (get_assets_by_user,
                        get_active_assets_by_user,
                        get_asset_by_id,
                        create_asset,
                        restore_asset_by_id,
                        update_asset,
                        delete_asset)

router = APIRouter()


@router.get("/", response_model=List[AssetResponse])
async def get_my_assets(current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    """Получить все активные валюты текущего пользователя"""
    assets = await get_active_assets_by_user(db, current_user.id)
    return assets


@router.get("/all", response_model=List[AssetResponse])
async def get_all_my_assets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    """Получить все валюты текущего пользователя (включая неактивные)"""
    assets = await get_assets_by_user(db, current_user.id)
    return assets


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: int,
                    current_user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    """Получить конкретный актив по ID"""
    asset = await get_asset_by_id(db, asset_id, current_user.id)

    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.post("/", response_model=AssetResponse)
async def create_new_asset(asset_data: AssetCreateRequest,
                           current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    """Создать новый актив для отслеживания"""
    asset = await create_asset(db, asset_data, current_user.id)
    return asset


@router.post("/{asset_id}/restore", response_model=AssetResponse)
async def restore_asset(asset_id: int,
                        current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    """Восстановить неактивный актив"""
    asset = await restore_asset_by_id(db, asset_id, current_user.id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_existing_asset(asset_id: int,
                                asset_data: AssetUpdateRequest,
                                current_user: User = Depends(get_current_user),
                                db: AsyncSession = Depends(get_db)):
    """Обновить данные актива"""
    asset = await update_asset(db, asset_id, asset_data, current_user.id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.delete("/{asset_id}")
async def delete_existing_asset(asset_id: int,
                                current_user: User = Depends(get_current_user),
                                db: AsyncSession = Depends(get_db)):
    """Удалить валюту"""
    result = await delete_asset(db, asset_id, current_user.id)
    if not result:
        raise HTTPException(404, "Asset not found")
    return {"message": "Asset deleted successfully"}
import asyncio
from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import async_session
from services.price_service import get_current_price
from crud.asset import get_all_active_assets, update_asset_price
from services.celery_app import celery_app

async def update_all_assets_prices():
    """
    Асинхронная функция для обновления цен всех активов
    """
    async with async_session() as session:
        try:
            assets = await get_all_active_assets(session)

            updated_count = 0
            for asset in assets:
                current_price = await get_current_price(asset.symbol)
                if current_price is not None:
                    await update_asset_price(session, asset.id, current_price)
                    updated_count += 1
                    print(f"Updated {asset.symbol}: ${current_price}")
                else:
                    print(f"Failed to get price for {asset.symbol}")
                await asyncio.sleep(0.1)

            print(f"Successfully updated {updated_count}/{len(assets)} assets")
            return updated_count

        except Exception as e:
            print(f"Error updating prices: {e}")
            await session.rollback()
            return 0


@celery_app.task(name="update_prices_task")
def update_prices_task():
    """
    Celery задача для обновления цен
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(update_all_assets_prices())
        else:
            return loop.run_until_complete(update_all_assets_prices())
    except RuntimeError:
        return asyncio.run(update_all_assets_prices())


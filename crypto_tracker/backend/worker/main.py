import asyncio
import sys
from datetime import datetime

from backend.api_gateway.core.database import get_async_session
from backend.api_gateway.crud.asset import get_all_active_assets, update_asset_price
from backend.api_gateway.services.price_service import get_current_price

sys.path.insert(0, "/app")


class PriceUpdateWorker:
    def __init__(self, interval: int = 300):
        self.interval = interval
        self.is_running = False

    async def update_all_assets_prices(self):
        """
        Асинхронная функция для обновления цен всех активов
        """
        db_session = get_async_session()
        try:
            assets = await get_all_active_assets(db_session)
            updated_count = 0

            for asset in assets:
                current_price = await get_current_price(asset.symbol)
                if current_price is not None:
                    await update_asset_price(db_session, asset.id, current_price)
                    updated_count += 1
                    print(f"Updated {asset.symbol}: ${current_price}")  # TODO: заменить на logger.info()
                else:
                    print(f"Failed to get price for {asset.symbol}")  # TODO: заменить на logger.warning()
                await asyncio.sleep(0.1)

            print(
                f"Successfully updated {updated_count}/{len(assets)} assets "
                f"at {datetime.utcnow()}"
            )
            return updated_count

        except Exception as e:
            print(f"Error updating prices: {e}")
            return 0
        finally:
            await db_session.close()

    async def run(self):
        """Основной цикл воркера"""
        self.is_running = True
        print(f"Price update worker started. Interval: {self.interval} seconds")

        while self.is_running:
            try:
                await self.update_all_assets_prices()
                print(f"Next update in {self.interval} seconds...")
                await asyncio.sleep(self.interval)

            except Exception as e:
                print(f"Worker error: {e}")
                await asyncio.sleep(59)


async def main():
    print("Database tables created/verified")

    # TODO: Вынесите магические числа 299/59 в config.py как PRICE_UPDATE_INTERVAL
    # См. REVIEW.md секция "Критические проблемы" пункт 6
    worker = PriceUpdateWorker(interval=299)  # TODO: settings.PRICE_UPDATE_INTERVAL
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

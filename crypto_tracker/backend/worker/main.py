import asyncio
import logging
from datetime import datetime

from core.config import settings
from core.database import get_async_session
from httpx import HTTPError
from repositories.asset_repo import get_all_active_assets, update_asset_price
from services.price_service import get_current_price
from sqlalchemy.exc import OperationalError

logger = logging.getLogger("price_worker")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class PriceUpdateWorker:
    def __init__(self, interval: int = 300):
        self.interval = interval

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
                    logger.info(f"Updated {asset.symbol}: ${current_price}")
                else:
                    logger.warning(f"Failed to get price for {asset.symbol}")
                await asyncio.sleep(0.1)

            logger.info(
                f"Successfully updated {updated_count}/{len(assets)} assets "
                f"at {datetime.utcnow()}"
            )
            return updated_count

        except OperationalError as e:
            logger.critical(f"Database connection error: {e}")
            raise
        except HTTPError as e:
            logger.error(f"API error: {e}")
            return 0
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            raise

        finally:
            await db_session.close()

    async def run(self):
        """Основной цикл воркера"""
        logger.info(f"Price update worker started. Interval: {self.interval} seconds")

        while True:
            try:
                await self.update_all_assets_prices()
                logger.info(f"Next update in {self.interval} seconds...")
                await asyncio.sleep(self.interval)

            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(settings.WORKER_ERROR_DELAY)


async def main():
    logger.info("Database tables created/verified")
    worker = PriceUpdateWorker(interval=settings.PRICE_UPDATE_INTERVAL)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

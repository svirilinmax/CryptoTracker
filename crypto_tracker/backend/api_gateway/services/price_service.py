import logging
from typing import Optional

import aiohttp
from core.config import settings

logger = logging.getLogger("price_api_getaway")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

SYMBOL_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "ADA": "cardano",
    "DOT": "polkadot",
    "SOL": "solana",
}


def symbol_to_id(symbol: str) -> str:
    """
    Конвертирует символ (BTC, ETH…) в ID для CoinGecko API.
    """
    return SYMBOL_MAP.get(symbol.upper(), symbol.lower())


async def get_current_price(symbol: str) -> Optional[float]:
    """
    Получить текущую цену криптовалюты.
    """
    coin_id = symbol_to_id(symbol)
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {"x-cg-demo-api-key": settings.CRYPTO_API_KEY}
    params = {"ids": coin_id, "vs_currencies": "usd"}

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    price = data.get(coin_id, {}).get("usd")
                    if price is None or price <= 0 or price > 1_000_000_000:
                        logger.warning(f"Invalid price received: {price}")
                        return None
                    return float(price)

                print(f"API error {response.status}")
                return None

    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

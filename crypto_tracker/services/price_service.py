import aiohttp
from typing import Optional
from core.config import settings

SYMBOL_MAP = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'ADA': 'cardano',
    'DOT': 'polkadot',
    'SOL': 'solana',
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
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get(coin_id, {}).get("usd")

                print(f"API error {response.status}")
                return None

    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

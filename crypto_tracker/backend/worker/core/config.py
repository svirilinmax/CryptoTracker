from pathlib import Path

from pydantic_settings import BaseSettings

BACKEND_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str
    CRYPTO_API_KEY: str

    PRICE_UPDATE_INTERVAL: int = 300  # 5 минут по умолчанию
    WORKER_ERROR_DELAY: int = 60  # 1 минута при ошибках
    SENTRY_DSN: str = ""

    class Config:
        env_file = BACKEND_DIR / ".env"


settings = Settings()

from pathlib import Path

from pydantic_settings import BaseSettings

BACKEND_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    CRYPTO_API_KEY: str
    DATABASE_URL: str = (
        "postgresql://crypto_user:crypto_password@postgres:5432/crypto_db"
    )
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str
    SECRET_KEY: str
    SENTRY_DSN: str

    # Настройки для воркера
    PRICE_UPDATE_INTERVAL: int = 300  # 5 минут по умолчанию
    WORKER_ERROR_DELAY: int = 60  # 1 минута при ошибках

    class Config:
        env_file = BACKEND_DIR / ".env"


settings = Settings()

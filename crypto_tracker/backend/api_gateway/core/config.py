from pathlib import Path

from pydantic_settings import BaseSettings

BACKEND_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    CRYPTO_API_KEY: str
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str
    SECRET_KEY: str
    SENTRY_DSN: str

    class Config:
        env_file = BACKEND_DIR / ".env"


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    CRYPTO_API_KEY: str
    DATABASE_URL: str = "postgresql://crypto_user:crypto_password@postgres:5432/crypto_db"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
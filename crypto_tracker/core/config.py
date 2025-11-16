from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CRYPTO_API_KEY: str = "CG-QAa7MVJ3Q1korNz14usWqcBa"
    DATABASE_URL: str = "sqlite+aiosqlite:///./crypto.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    #SECRET_KEY: str = "your-secret-key-here"

    class Config:
        env_file = ".env"


settings = Settings()
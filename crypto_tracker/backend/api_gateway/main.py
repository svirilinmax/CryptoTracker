import sys
from datetime import datetime

import sentry_sdk
from backend.api_gateway.api.v1.routers import api_router
from backend.api_gateway.core.database import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, "/app")

# TODO: КРИТИЧНО! Переместите Sentry DSN в .env файл
# Секретный ключ попадает в Git и может быть скомпрометирован
# См. REVIEW.md секция "Критические проблемы" пункт 1
# Решение: dsn=settings.SENTRY_DSN из config.py
sentry_sdk.init(
    dsn="https://1809f68dab6b0663dc34b2b35ba87b39@o4510421627502592."
    "ingest.de.sentry.io/4510421631959120",
    # Добавляем данные о пользователях (заголовки, IP и т.д.)
    send_default_pii=True,
    # Настройка сбора данных о производительности
    traces_sample_rate=1.0,
    # Включить профилирование (опционально)
    profiles_sample_rate=1.0,
)


app = FastAPI(title="Crypto Tracker API")

# Разрешаем фронту обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # при необходимости ограничь домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API роуты
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Асинхронное создание таблиц при старте"""
    # TODO: КРИТИЧНО! Удалите create_tables() и используйте Alembic миграции
    # При изменении моделей ТЕРЯЮТСЯ ВСЕ ДАННЫЕ пользователей!
    # См. REVIEW.md секция "Критические проблемы" пункт 2
    # Команды: alembic init alembic -> alembic revision --autogenerate -m "Init" -> alembic upgrade head
    await create_tables()
    print("Таблицы базы данных созданы")

    for route in app.routes:
        if hasattr(route, "path"):
            print(f"🔍 Route: {route.path}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}


@app.get("/")
async def root():
    """Главная страница — будем отдавать index.html??"""
    return {"message": "Crypto Tracker API работает!"}


@app.get("/sentry-debug")
async def trigger_error():
    """Эндпоинт для тестирования Sentry - вызывает ошибку деления на ноль"""
    division_by_zero = 1 / 0
    return {"message": f"This should never be reached {division_by_zero}"}

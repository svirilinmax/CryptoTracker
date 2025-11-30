from datetime import datetime

import sentry_sdk
from api.v1.routers import api_router
from core.config import settings
from core.database import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Добавляем данные о пользователях (заголовки, IP и т.д.)
    send_default_pii=True,
    # Настройка сбора данных о производительности
    traces_sample_rate=1.0,
    # Включить профилирование (опционально)
    profiles_sample_rate=1.0,
)


app = FastAPI(
    title="Crypto Tracker API",
    description="API для отслеживания цен криптовалют с уведомлениями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

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

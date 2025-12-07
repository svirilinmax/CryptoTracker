from datetime import datetime

import sentry_sdk
from api.v1.routers import api_router
from core.config import settings
from core.database import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]


def scrub_sensitive_data(event, hint):
    if "request" in event:
        if "headers" in event["request"]:
            event["request"]["headers"].pop("Authorization", None)
    return event


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=False,
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    before_send=scrub_sensitive_data,
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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

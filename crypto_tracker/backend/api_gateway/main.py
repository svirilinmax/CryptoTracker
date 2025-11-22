import sys
import os

sys.path.insert(0, '/app')


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from backend.api_gateway.core.database import create_tables
from backend.api_gateway.api.v1.routers import api_router

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
    await create_tables()
    print("Таблицы базы данных созданы")

    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"🔍 Route: {route.path}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/")
async def root():
    """Главная страница — будем отдавать index.html??"""
    return {"message": "Crypto Tracker API работает!"}
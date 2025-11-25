# 📋 Code Review: Crypto Tracker

**Оценка:** 8/10 ⭐

Проект представляет собой продвинутую систему отслеживания криптовалют с автоматическим обновлением цен, JWT аутентификацией и фоновыми задачами. Код демонстрирует хорошее понимание современного Python стека, асинхронного программирования и микросервисной архитектуры.

---

## ✅ Сильные стороны

### 1. **Профессиональная архитектура** 🏗️
- Четкое разделение на API Gateway и Worker
- Микросервисный подход с Docker Compose
- Использование SQLAlchemy 2.0 с async/await
- Интеграция с PostgreSQL и Redis

### 2. **Современный стек технологий** 🚀
- **FastAPI** с полным async
- **AsyncPG** для асинхронной работы с БД
- **AIOHTTP** для внешних API запросов
- **Sentry** для мониторинга ошибок

### 3. **JWT аутентификация** 🔐
```python
# security.py - использование PBKDF2 для хеширования паролей
def make_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)
```

### 4. **Фоновая обработка** ⏰
```python
# worker/main.py - автоматическое обновление цен каждые 5 минут
class PriceUpdateWorker:
    async def update_all_assets_prices(self):
        assets = await get_all_active_assets(db_session)
        for asset in assets:
            current_price = await get_current_price(asset.symbol)
```

### 5. **RESTful API дизайн** 📡
- Правильное использование HTTP методов (GET, POST, PUT, DELETE)
- Версионирование API (`/api/v1/`)
- Защита эндпоинтов через `Depends(get_current_user)`

### 6. **История цен** 📊
```python
# models/database.py - отдельная таблица для исторических данных
class PriceHistory(Base):
    asset_id = Column(Integer, ForeignKey("assets.id"))
    price = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)
```

### 7. **Docker контейнеризация** 🐳
- Multi-service setup (postgres, redis, api, worker, frontend)
- Правильное управление зависимостями через `depends_on`

### 8. **CORS настройка** 🌐
```python
# main.py - поддержка фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)
```

### 9. **Health check эндпоинт** ❤️
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

### 10. **Relationship в SQLAlchemy** 🔗
```python
# Правильное использование back_populates
class User(Base):
    assets = relationship("Asset", back_populates="user")

class Asset(Base):
    user = relationship("User", back_populates="assets")
```

---

## 🔴 Критические проблемы

### 1. **HARDCODED Sentry DSN в коде** 🚨
**Файл:** `backend/api_gateway/main.py:14`

```python
# ❌ ПЛОХО: секретные данные в коде
sentry_sdk.init(
    dsn="https://1809f68dab6b0663dc34b2b35ba87b39@o4510421627502592."
    "ingest.de.sentry.io/4510421631959120",
```

**Проблема:** Sentry DSN содержит секретный ключ и попадет в Git историю

**Решение:**
```python
# ✅ ХОРОШО: переместить в .env
from backend.api_gateway.core.config import settings

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,  # берем из переменных окружения
    send_default_pii=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
```

В `core/config.py`:
```python
class Settings(BaseSettings):
    SENTRY_DSN: str = ""  # пустая строка = отключен
```

В `.env`:
```
SENTRY_DSN=https://your_key@sentry.io/project_id
```

---

### 2. **Base.metadata.create_all() вместо миграций** ⚠️
**Файл:** `backend/api_gateway/main.py:45`

```python
# ❌ ПРОБЛЕМА: пересоздает таблицы при каждом запуске
@app.on_event("startup")
async def startup_event():
    await create_tables()
```

**Почему это плохо:**
- При изменении моделей **ТЕРЯЮТСЯ ДАННЫЕ** пользователей
- Нет контроля версий схемы БД
- Невозможен откат к предыдущей версии

**Решение:** Использовать Alembic для миграций

```bash
# Инициализация
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "Initial tables"

# Применение миграций
alembic upgrade head
```

Убрать из `startup_event`:
```python
@app.on_event("startup")
async def startup_event():
    # await create_tables()  # ❌ УДАЛИТЬ
    print("API started")
```

---

### 3. **Отсутствие валидации в Pydantic схемах** 📝
**Файл:** `backend/api_gateway/models/schemas.py`

```python
# ❌ ПРОБЛЕМА: нет ограничений
class AssetBase(BaseModel):
    symbol: str  # что если ""? или "x"*1000?
    min_price: float  # может быть отрицательной?
    max_price: float  # может быть меньше min_price?
```

**Решение:**
```python
from pydantic import BaseModel, Field, field_validator

class AssetBase(BaseModel):
    symbol: str = Field(..., min_length=2, max_length=10, pattern="^[A-Z]+$")
    min_price: float = Field(..., gt=0, description="Должна быть > 0")
    max_price: float = Field(..., gt=0)

    @field_validator('max_price')
    @classmethod
    def validate_max_price(cls, v, info):
        if 'min_price' in info.data and v <= info.data['min_price']:
            raise ValueError('max_price должна быть > min_price')
        return v
```

---

### 4. **Отсутствие обработки ошибок БД** 💥
**Файл:** `backend/api_gateway/crud/user.py:24`

```python
# ❌ ПРОБЛЕМА: нет try/except для дублирования email/username
async def create_user(db: AsyncSession, user_data: UserCreateRequest):
    hashed_password = make_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
    )
    db.add(db_user)
    await db.commit()  # может упасть с IntegrityError
```

**Решение:**
```python
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

async def create_user(db: AsyncSession, user_data: UserCreateRequest):
    hashed_password = make_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
    )

    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        # Определяем какое поле вызвало ошибку
        if "email" in str(e.orig):
            raise HTTPException(400, "Email уже занят")
        elif "username" in str(e.orig):
            raise HTTPException(400, "Username уже занят")
        else:
            raise HTTPException(500, "Ошибка создания пользователя")
```

---

### 5. **get_db() без обработки ошибок транзакций** 🔄
**Файл:** `backend/api_gateway/core/database.py:14`

```python
# ❌ ПРОБЛЕМА: нет commit/rollback при ошибках
async def get_db():
    async with async_session() as session:
        yield session
```

**Решение:**
```python
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

### 6. **Хардкод в Worker интервалах** ⏱️
**Файл:** `backend/worker/main.py:68`

```python
# ❌ ПРОБЛЕМА: магические числа 299, 59
worker = PriceUpdateWorker(interval=299)
await asyncio.sleep(59)
```

**Решение:**
```python
# В core/config.py
class Settings(BaseSettings):
    PRICE_UPDATE_INTERVAL: int = 300  # 5 минут
    ERROR_RETRY_INTERVAL: int = 60

# В worker/main.py
from backend.api_gateway.core.config import settings

worker = PriceUpdateWorker(interval=settings.PRICE_UPDATE_INTERVAL)
await asyncio.sleep(settings.ERROR_RETRY_INTERVAL)
```

---

### 7. **Отсутствие пагинации в price history** 📄
**Файл:** `backend/api_gateway/crud/price_history.py:22`

```python
# ⚠️ ПРОБЛЕМА: hardcoded limit=100
async def get_price_history_by_asset(
    db: AsyncSession, asset_id: int, limit: int = 100
):
    # Что если история содержит миллионы записей?
```

**Решение:**
```python
async def get_price_history_by_asset(
    db: AsyncSession,
    asset_id: int,
    skip: int = 0,
    limit: int = 50  # меньше default
):
    if limit > 1000:  # защита от больших запросов
        limit = 1000

    result = await db.execute(
        select(PriceHistory)
        .where(PriceHistory.asset_id == asset_id)
        .order_by(PriceHistory.recorded_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
```

В эндпоинте:
```python
@router.get("/{asset_id}/history")
async def get_asset_history(
    asset_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    history = await get_price_history_by_asset(db, asset_id, skip, limit)
    return history
```

---

## 💡 Рекомендации

### 1. **Добавить Logging вместо print()** 📝
```python
# ❌ ПЛОХО
print(f"Updated {asset.symbol}: ${current_price}")
print(f"Error fetching price: {e}")

# ✅ ХОРОШО
import logging

logger = logging.getLogger(__name__)

logger.info(f"Updated {asset.symbol}: ${current_price}")
logger.error(f"Error fetching price: {e}", exc_info=True)
```

Настройка:
```python
# main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

### 2. **Добавить Rate Limiting** 🛡️
```python
# Установить
pip install slowapi

# main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# В эндпоинте
@router.post("/register")
@limiter.limit("5/hour")  # 5 регистраций в час с одного IP
async def register(request: Request, user_data: UserCreateRequest):
    ...
```

---

### 3. **Расширить тесты** 🧪
Создать `tests/test_api.py`:
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepass123"
        })
        assert response.status_code == 200
        assert "id" in response.json()

@pytest.mark.asyncio
async def test_create_asset_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/assets/", json={
            "symbol": "BTC",
            "min_price": 30000,
            "max_price": 50000
        })
        assert response.status_code == 401
```

---

### 4. **Добавить модель Alert** 🔔
Как указано в `.env.add`, реализовать уведомления:

```python
# models/database.py
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    message = Column(String)
    alert_type = Column(String)  # "above_max", "below_min"
    price_at_alert = Column(Float)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    asset = relationship("Asset")
```

В Worker:
```python
async def check_price_alerts(self, asset, current_price):
    if current_price > asset.max_price:
        await create_alert(
            db, asset.user_id, asset.id,
            f"{asset.symbol} превысила {asset.max_price}$",
            "above_max", current_price
        )
    elif current_price < asset.min_price:
        await create_alert(
            db, asset.user_id, asset.id,
            f"{asset.symbol} упала ниже {asset.min_price}$",
            "below_min", current_price
        )
```

---

### 5. **Улучшить обработку CoinGecko API ошибок** 🌐
**Файл:** `backend/api_gateway/services/price_service.py`

```python
async def get_current_price(symbol: str, retry_count: int = 3) -> Optional[float]:
    coin_id = symbol_to_id(symbol)
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {"x-cg-demo-api-key": settings.CRYPTO_API_KEY}
    params = {"ids": coin_id, "vs_currencies": "usd"}

    for attempt in range(retry_count):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        price = data.get(coin_id, {}).get("usd")
                        if price is None:
                            logger.warning(f"Price not found for {coin_id}")
                        return price
                    elif response.status == 429:  # Rate limit
                        wait_time = int(response.headers.get('Retry-After', 60))
                        logger.warning(f"Rate limited, waiting {wait_time}s")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"API error {response.status}: {await response.text()}")
                        return None

        except asyncio.TimeoutError:
            logger.warning(f"Timeout fetching price for {symbol}, attempt {attempt + 1}/{retry_count}")
            await asyncio.sleep(2 ** attempt)  # exponential backoff
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}", exc_info=True)
            return None

    return None
```

---

### 6. **Добавить кэширование в Redis** 🚀
```python
# services/cache_service.py
import json
from backend.api_gateway.core.config import settings
import redis.asyncio as redis

redis_client = redis.from_url(settings.REDIS_URL)

async def get_cached_price(symbol: str) -> Optional[float]:
    cached = await redis_client.get(f"price:{symbol}")
    if cached:
        return float(cached)
    return None

async def cache_price(symbol: str, price: float, ttl: int = 60):
    await redis_client.setex(f"price:{symbol}", ttl, str(price))

# В price_service.py
async def get_current_price(symbol: str) -> Optional[float]:
    # Сначала проверяем кэш
    cached = await get_cached_price(symbol)
    if cached:
        return cached

    # Если нет - запрашиваем API
    price = await fetch_price_from_api(symbol)
    if price:
        await cache_price(symbol, price)
    return price
```

---

### 7. **Улучшить Docker Compose** 🐳
```yaml
# backend/docker-compose.yml
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: crypto_db
      POSTGRES_USER: crypto_user
      POSTGRES_PASSWORD: crypto_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:  # ✅ Добавить health check
      test: ["CMD-SHELL", "pg_isready -U crypto_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    depends_on:
      postgres:
        condition: service_healthy  # ✅ Ждем готовности БД
      redis:
        condition: service_healthy
    restart: unless-stopped  # ✅ Автоматический перезапуск

  worker:
    depends_on:
      api:
        condition: service_started  # ✅ Ждем API
    restart: unless-stopped

volumes:
  postgres_data:
```

---

### 8. **Добавить lifespan events** 🔄
```python
# main.py
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting up...")
    # await create_tables()  # Только для dev

    yield

    # Shutdown
    print("🛑 Shutting down...")
    await engine.dispose()

app = FastAPI(title="Crypto Tracker API", lifespan=lifespan)
```

---

### 9. **Добавить документацию Swagger** 📚
```python
# main.py
app = FastAPI(
    title="Crypto Tracker API",
    description="API для отслеживания цен криптовалют с уведомлениями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# В эндпоинтах
@router.post("/", response_model=AssetResponse,
             summary="Создать новый актив",
             description="Добавляет криптовалюту для отслеживания с min/max ценами")
async def create_new_asset(
    asset_data: AssetCreateRequest = Body(..., example={
        "symbol": "BTC",
        "min_price": 30000.0,
        "max_price": 50000.0
    }),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создает новый актив для отслеживания:
    - **symbol**: Символ криптовалюты (BTC, ETH, SOL и т.д.)
    - **min_price**: Нижний порог для уведомления
    - **max_price**: Верхний порог для уведомления
    """
    asset = await create_asset(db, asset_data, current_user.id)
    return asset
```

---

### 10. **Добавить мониторинг производительности** 📊
```python
# middleware/timing.py
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # Логируем медленные запросы
    if process_time > 1.0:
        logger.warning(f"Slow request: {request.url.path} took {process_time:.2f}s")

    return response
```

---

## 📊 Оценка по критериям

| Критерий | Оценка | Комментарий |
|----------|---------|-------------|
| **Архитектура** | 9/10 | Отличное разделение на сервисы, async/await |
| **Безопасность** | 7/10 | PBKDF2 хорошо, но hardcoded Sentry DSN |
| **База данных** | 8/10 | Правильные relationships, но нет миграций |
| **Обработка ошибок** | 6/10 | Нет try/except в CRUD, нет rollback |
| **Валидация** | 6/10 | Базовая Pydantic, нет Field с ограничениями |
| **Тестирование** | 3/10 | Отсутствуют тесты |
| **Документация** | 8/10 | Отличный README, комментарии в коде |
| **Docker** | 9/10 | Полный compose с 5 сервисами |
| **Код-стайл** | 8/10 | Чистый код, но print() вместо logging |
| **Масштабируемость** | 7/10 | Worker хорош, но нет rate limiting |

**Общая оценка:** 8.0/10 ⭐

---

## 🎯 План исправлений

### Критические (1-2 дня):
1. ✅ Переместить Sentry DSN в `.env` (5 минут)
2. ✅ Настроить Alembic миграции (1 час)
3. ✅ Добавить try/except в CRUD операции (30 минут)
4. ✅ Улучшить `get_db()` с commit/rollback (10 минут)
5. ✅ Добавить валидацию в Pydantic схемы (30 минут)

### Важные (3-5 дней):
6. ✅ Заменить print() на logging (1 час)
7. ✅ Реализовать модель Alert и логику уведомлений (4 часа)
8. ✅ Добавить пагинацию в history (30 минут)
9. ✅ Улучшить обработку CoinGecko API (1 час)
10. ✅ Написать базовые тесты (3 часа)

### Желательные (неделя):
11. ⚡ Настроить Redis кэширование (2 часа)
12. ⚡ Добавить rate limiting (1 час)
13. ⚡ Расширить Swagger документацию (2 часа)
14. ⚡ Добавить middleware для мониторинга (1 час)
15. ⚡ Улучшить Docker Compose с health checks (30 минут)

---

## 💬 Заключение

**Отличная работа!** 🎉 Проект демонстрирует:
- ✅ Глубокое понимание FastAPI и async Python
- ✅ Умение работать с микросервисами
- ✅ Продвинутое использование SQLAlchemy 2.0
- ✅ Интеграцию внешних API
- ✅ Docker контейнеризацию

**Главные достижения:**
1. Работающий Worker с автоматическим обновлением
2. JWT аутентификация с PBKDF2
3. Асинхронная архитектура end-to-end
4. Интеграция с Sentry для мониторинга

**Что улучшить:**
1. Миграции Alembic вместо create_all()
2. Секреты в .env (особенно Sentry DSN)
3. Обработка ошибок БД с rollback
4. Добавить тесты
5. Реализовать систему Alert

Это один из самых профессиональных проектов среди рассмотренных! С исправлением критических замечаний проект будет готов к production. 🚀

**Рекомендация:** Продолжайте развивать проект, добавьте WebSocket для real-time уведомлений и email рассылку при срабатывании alert'ов. 📧

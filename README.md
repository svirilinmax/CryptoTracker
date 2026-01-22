# Crypto Tracker

### Система для отслеживания цен криптовалют с фоновыми задачами

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-000000)](https://alembic.sqlalchemy.org/)
[![Sentry](https://img.shields.io/badge/Sentry-Monitoring-362D59?logo=sentry)](https://sentry.io/)

## Содержание

- [Функциональность](#функциональность)
- [Технологический стек](#технологический-стек)
- [Структура проекта](#структура-проекта)
- [Быстрый старт](#быстрый-старт)
- [Frontend интерфейс](#frontend-интерфейс)
- [API Endpoints](#api-endpoints)
- [База данных](#база-данных)
- [Безопасность](#безопасность)
- [Тестирование](#тестирование)
- [Конфигурация](#конфигурация)
- [Распространненые проблемы](#распространенные-проблемы)
- [Контакты](#контакты)

## Функциональность

- **Отслеживание криптовалют** - добавление криптоактивов для мониторинга
- **Автоматическое обновление цен** - фоновая задача обновляет цены с настраиваемым интервалом
- **История цен** - сохранение и просмотр исторических данных по ценам с пагинацией
- **Визуализация данных** - графики цен активов в реальном времени
- **REST API** - полноценное API для интеграции с фронтендом и мобильными приложениями
- **JWT аутентификация** - безопасная система аутентификации пользователей
- **Полноценный Frontend** - веб-интерфейс для управления активами
- **Мониторинг ошибок** - интеграция с Sentry для отслеживания ошибок и производительности

## Технологический стек

### Backend
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)](https://redis.io/)
[![AIOHTTP](https://img.shields.io/badge/AIOHTTP-3.9-2C5BB4?logo=aiohttp)](https://docs.aiohttp.org/)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens)](https://jwt.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0-E92063?logo=pydantic)](https://docs.pydantic.dev/)

### Frontend
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5)](https://developer.mozilla.org/ru/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3)](https://developer.mozilla.org/ru/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript)](https://developer.mozilla.org/ru/docs/Web/JavaScript)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.0-FF6384?logo=chart.js)](https://www.chartjs.org/)

### Инфраструктура
[![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Compose-2.20-2496ED?logo=docker)](https://docs.docker.com/compose/)
[![Sentry](https://img.shields.io/badge/Sentry-Monitoring-362D59?logo=sentry)](https://sentry.io/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-000000)](https://alembic.sqlalchemy.org/)

## Структура проекта

```
crypto_tracker/
├── backend/
│   ├── api_gateway/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/     # API endpoints (assets.py, auth.py)
│   │   │       └── routers.py     # Маршрутизация API
│   │   ├── core/                 # Конфигурация, БД, безопасность
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/               # Модели данных и схемы
│   │   │   ├── database.py       # SQLAlchemy модели
│   │   │   └── schemas.py        # Pydantic схемы
│   │   ├── repositories/         # Паттерн репозиторий для работы с БД
│   │   │   ├── asset.py
│   │   │   ├── price_history.py
│   │   │   └── user.py
│   │   ├── services/             # Бизнес-логика
│   │   │   └── price_service.py  # Сервис работы с ценами
│   │   ├── alembic/              # Миграции базы данных
│   │   ├── main.py               # Точка входа API
│   │   └── requirements.txt
│   ├── worker/                   # Фоновые задачи
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── database.py
│   │   │   ├── schemas.py
│   │   │   └── __init__.py
│   │   ├── repositories/
│   │   │   ├── asset_repo.py
│   │   │   ├── price_repo.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── price_service.py
│   │   │   └── __init__.py
│   │   ├── main.py
│   │   └── requirements_worker.txt
│   └── docker-compose.yml
├── frontend/                     # Статические файлы фронтенда
│   ├── index.html               # Главная страница с адаптивным интерфейсом
│   ├── login.html               # Страница входа
│   ├── register.html            # Страница регистрации
│   ├── graph_of_asset.html      # Страница с графиком цен актива
│   └── Dockerfile
├── tests/                        # Тесты
│   ├── test_api.py              # API тесты
│   ├── database_models_test.py  # Тесты моделей данных (в разработке)
│   └── __init__.py
├── .env                         # Переменные окружения
├── .pre-commit-config.yaml     # Конфигурация pre-commit
├── Makefile                    # Утилиты для разработки
└── README.md                   # Документация
```

## Быстрый старт

### Предварительные требования

- [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/)
- [CoinGecko API ключ](https://www.coingecko.com/en/api) (бесплатный)
- [Sentry аккаунт](https://sentry.io/signup/) (бесплатный) - для мониторинга ошибок

### Установка и запуск

1. **Клонирование и настройка**:
```bash
   git clone https://github.com/svirilinmax/CryptoTracker.git
   cd crypto_tracker
```

2. **Настройка переменных окружения**:
```bash
   cp .env.example .env
```
Отредактируйте `.env` файл:
```env
CRYPTO_API_KEY=your_coingecko_api_key_here
JWT_SECRET=your_super_secret_jwt_key
SECRET_KEY=your_fastapi_secret_key
SENTRY_DSN=your_sentry_dsn_here
PRICE_UPDATE_INTERVAL=300
WORKER_ERROR_DELAY=60
DATABASE_URL=postgresql://crypto_user:crypto_password@postgres:5432/crypto_db
REDIS_URL=redis://redis:6379/0
```

3. **Запуск приложения**:
```bash
   docker-compose up --build -d
```

### Доступные сервисы

| Сервис | URL | Описание |
|--------|-----|----------|
| **Frontend** | http://localhost:8080 | Веб-интерфейс приложения |
| **API** | http://localhost:8005 | Основное REST API |
| **API Documentation** | http://localhost:8005/docs | Swagger UI документация |
| **Health Check** | http://localhost:8005/health | Проверка состояния API |
| **Sentry Test** | http://localhost:8005/sentry-debug | Тестовый endpoint для Sentry |

## Frontend интерфейс

### Основные страницы

1. **Главная страница (`index.html`)**
   - Адаптивный интерфейс для гостей и авторизованных пользователей
   - Отображение списка активов с текущими ценами
   - Форма добавления новых активов с валидацией
   - Автоматическая проверка авторизации

2. **Регистрация (`register.html`)**
   - Форма регистрации с полями: имя, email, пароль
   - Валидация данных на стороне клиента
   - Интеграция с API аутентификации

3. **Вход (`login.html`)**
   - Форма входа с email и паролем
   - Сохранение JWT токена в localStorage
   - Обработка ошибок аутентификации

4. **График цен (`graph_of_asset.html`)**
   - Визуализация истории цен актива
   - Автоматическое обновление графика каждые 6 секунд
   - Адаптивные столбчатые диаграммы
   - Навигация обратно к списку активов

### Особенности Frontend
- **Адаптивная верстка** для разных устройств
- **Динамическое обновление** интерфейса без перезагрузки страницы
- **JWT-аутентификация** с токенами в localStorage
- **Обработка ошибок** с пользовательскими сообщениями
- **Интуитивный UX** с понятной навигацией

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация пользователя
- `POST /api/v1/auth/login` - Вход в систему
- `GET /api/v1/auth/me` - Получение информации о текущем пользователе

### Управление активами
- `GET /api/v1/assets/` - Получить активные активы текущего пользователя
- `GET /api/v1/assets/all` - Получить все активы (включая неактивные)
- `POST /api/v1/assets/` - Создать новый актив
- `GET /api/v1/assets/{asset_id}` - Получить конкретный актив
- `PUT /api/v1/assets/{asset_id}` - Обновить актив
- `DELETE /api/v1/assets/{asset_id}` - Удалить актив (деактивировать)
- `POST /api/v1/assets/{asset_id}/restore` - Восстановить актив
- `GET /api/v1/assets/{asset_id}/history` - Получить историю цен с пагинацией

### Системные
- `GET /health` - Проверка здоровья приложения
- `GET /sentry-debug` - Тестовый endpoint для проверки Sentry

## База данных

### Модели данных

#### Пользователь (User)
- `id` - Integer, Primary Key
- `username` - String(50), уникальный, 3-50 символов
- `email` - String(255), уникальный
- `password_hash` - String(255)
- `is_active` - Boolean, default=True
- `created_at` - DateTime, default=datetime.utcnow

#### Актив (Asset)
- `id` - Integer, Primary Key
- `user_id` - Integer, ForeignKey('users.id')
- `symbol` - String(10), заглавные буквы
- `min_price` - Float, положительное число
- `max_price` - Float, положительное число, > min_price
- `current_price` - Float, nullable
- `is_active` - Boolean, default=True
- `created_at` - DateTime, default=datetime.utcnow

#### История цен (PriceHistory)
- `id` - Integer, Primary Key
- `asset_id` - Integer, ForeignKey('assets.id')
- `price` - Float, положительное число
- `recorded_at` - DateTime, default=datetime.utcnow, индекс для оптимизации запросов

### Миграции с Alembic

```bash
   # Применить миграции
   docker-compose exec api alembic upgrade head
   
   # Создать новую миграцию
   docker-compose exec api alembic revision --autogenerate -m "Описание изменений"
   
   # Откатить миграцию
   docker-compose exec api alembic downgrade -1
```

## Безопасность

- **PBKDF2-SHA256** для хеширования паролей
- **JWT токены** с 7-дневным сроком действия
- **HTTPS-подготовка** (рекомендуется для продакшена)
- **CORS** настройки для фронтенда
- **Валидация входных данных** на всех уровнях
- **Защита от SQL-инъекций** через SQLAlchemy
- **Sentry мониторинг** для отслеживания уязвимостей

## Тестирование

### Типы тестов (в разработке)

1. **API тесты** (`test_api.py`)
   - Тестирование endpoints
   - Проверка авторизации
   - Валидация ответов

2. **Тесты моделей данных** (`database_models_test.py`)
   - Валидация Pydantic схем
   - Тестирование ограничений полей
   - Проверка типов данных

### Запуск тестов

```bash
   # Запуск всех тестов
   pytest
   
   # Запуск конкретного тестового файла
   pytest tests/database_models_test.py
   
   # С отчетом о покрытии
   pytest --cov=backend tests/
```

## Конфигурация

### Поддерживаемые криптовалюты
- BTC (Bitcoin)
- ETH (Ethereum)
- ADA (Cardano)
- DOT (Polkadot)
- SOL (Solana)

### Настройка интервалов
- `PRICE_UPDATE_INTERVAL` - интервал обновления цен в секундах (по умолчанию 300)
- `WORKER_ERROR_DELAY` - задержка при ошибках воркера (по умолчанию 60)
- `GRAPH_UPDATE_INTERVAL` - интервал обновления графиков (6000 мс)


## Распространенные проблемы

1. **Ошибки авторизации**:
```javascript
// Проверка токена
const token = localStorage.getItem("access_token");
if (!token) window.location.href = "/login.html";
```

2. **Проблемы с графиками**:
   - Проверьте, что asset_id передается в URL
   - Убедитесь, что коэффициенты расчета высоты корректны
   - Проверьте CORS настройки backend

3. **Ошибки API запросов**:
   - Проверьте заголовки Authorization
   - Убедитесь, что API доступен по указанному URL
   - Проверьте формат JSON данных

### Полезные команды для диагностики

```bash
   # Проверить статус контейнеров
   docker-compose ps
   
   # Просмотреть логи фронтенда
   docker-compose logs frontend
   
   # Проверить API ответы
   curl http://localhost:8005/health
   curl -H "Authorization: Bearer <token>" http://localhost:8005/api/v1/assets
```
## Контакты

Проект разработан в рамках демонстрации умений на позицию Junior Backend Developer.

По вопросам и предложениям:
- **Telegram**: [@maxsvirilin](https://t.me/svirilinmax)
- **Email**: [mak.svirilin@gmail.com](mailto:mak.svirilin@gmail.com)

## Лицензия

Этот проект выпущен на условиях лицензии MIT. Подробности см. в файле `LICENSE`.

## Вклад в проект

1. Форкните репозиторий
2. Создайте feature ветку: `git checkout -b feature/amazing-feature`
3. Внесите изменения и добавьте тесты
4. Запустите тесты: `pytest`
5. Запустите pre-commit: `pre-commit run --all-files`
6. Создайте Pull Request

---

**Crypto Tracker** - полнофункциональная система для отслеживания криптовалютных активов с современным веб-интерфейсом, надежным бэкендом и лучшими практиками разработки.
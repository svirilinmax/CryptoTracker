# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY ../requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВЕСЬ проект (из родительской папки)
COPY .. .

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app

# Запускаем приложение
CMD ["sh", "-c", "alembic upgrade head && uvicorn backend.api_gateway.main:app --host 0.0.0.0 --port 8000"]

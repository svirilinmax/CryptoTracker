# backend/worker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости из текущей директории (backend/)
COPY ../../requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

ENV PYTHONPATH=/app

# Запускаем worker
CMD ["sh", "-c", "alembic upgrade head && python -m backend.worker.main"]

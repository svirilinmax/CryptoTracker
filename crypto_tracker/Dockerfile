# Базовый образ - Python 3.11 с минимальными компонентами
FROM python:3.11-slim

# Создаем непривилегированного пользователя и группу
RUN groupadd -r celeryuser && useradd -r -g celeryuser celeryuser

# Рабочая директория внутри контейнера
WORKDIR /crypto_traker

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем Python-библиотеки из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем curl для healthcheck (если его нет)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Копируем основной код приложения
COPY . .

# Меняем владельца файлов на celeryuser
RUN chown -R celeryuser:celeryuser /crypto_traker

# Документируем какой порт использует приложение
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда запуска при старте контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
from celery import Celery
from core.config import settings

celery_app = Celery(
    "crypto_tracker",
    broker=settings.REDIS_URL,  # Redis как брокер сообщений
    backend=settings.REDIS_URL, # Redis для хранения результатов
    include=["services.tasks"]  # задачи
)

# Настройка Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=60,
    broker_connection_retry_on_startup=True,
)

# Расписание задач
celery_app.conf.beat_schedule = {
    'update-prices-every-minute': {
        'task': 'update_prices_task',
        'schedule': 300.0,
    },
}
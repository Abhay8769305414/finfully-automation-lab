from celery import Celery
from src.config import Config

celery_app = Celery(
    "finfully_tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=["src.worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_always_eager=Config.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=True,
)

from celery import Celery
from celery.schedules import crontab

REDIS_URL = "redis://localhost:6379/0"

celery_app = Celery(
    "price_tracker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.checker_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Almaty",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "check-active-trackings-every-15-min": {
        "task": "app.tasks.checker_tasks.run_all_trackings_check",
        "schedule": crontab(minute="*/15"),  
    },
}
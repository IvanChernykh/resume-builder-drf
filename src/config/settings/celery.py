import os

from config.settings.settings import TIME_ZONE

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CELERY_REDIS_DB = int(os.getenv("REDIS_DB_CELERY", 5))

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_REDIS_DB}"
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_TRACK_STARTED = True

CELERY_TIMEZONE = TIME_ZONE

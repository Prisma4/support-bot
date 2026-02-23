from celery import Celery

from settings import Settings

settings = Settings()

app = Celery('bot_worker',
             broker=settings.celery_broker_url,
             backend=settings.celery_result_backend,
             include=['celery_worker.tasks'])

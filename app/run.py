import time

from celery import Celery

from core.config import settings

app = Celery(__name__)
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_BACKEND_URL
app.conf.timezone = settings.TIMEZONE


@app.task(name='create_task')
def create_task(a, b, c):
    time.sleep(a)
    return b + c

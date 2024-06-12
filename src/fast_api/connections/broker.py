import os

from celery import Celery

celery_app = Celery(
    broker=f"amqp://guest:guest@{os.environ.get('host')}:5672",
    backend="rpc://",
)

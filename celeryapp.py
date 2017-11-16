from celery import Celery
from tasks import config


app = Celery('proteomics-tasks')
app.conf.update(
    BROKER_HOST=config.BROKER_URL,
    BROKER_PORT=config.BROKER_PORT,
    CELERY_TASK_SERIALIZER=config.CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=config.CELERY_TASK_SERIALIZER,
    CELERY_ACCEPT_CONTENT=[config.CELERY_TASK_SERIALIZER],
    CELERY_RESULT_BACKEND=config.CELERY_RESULT_BACKEND,
    CELERYD_PREFETCH_MULTIPLIER=1,
)

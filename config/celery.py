#!/usr/bin/env python
import os
import logging

from celery import Celery, Task

from django.conf import settings


celery_fail_logger = logging.getLogger('celery-failed-tasks')

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


EXCEPTIONS = () # RuntimeError, HTTPError) # HAS TO BE A TUPLE
MAX_RETRIES = 10


class LoggingTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        celery_fail_logger.exception('Task failed: %s' % exc, exc_info=exc)
        super().on_failure(exc, task_id, args, kwargs, einfo)


class RetryingTask(Task):
    autoretry_for = EXCEPTIONS
    retry_kwargs = {'max_retries': MAX_RETRIES}
    retry_backoff = True
    retry_backoff_max = 60 * 60 * 1 # 1 hour
    retry_jitter = True  # randomness in backoff delay


class LoggingAndRetryingTask(RetryingTask, LoggingTask):
    pass


app = Celery('apps')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

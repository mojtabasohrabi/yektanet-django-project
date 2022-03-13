from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_task.settings')
app = Celery('celery_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "run-every-hour": {
        "task": "tasks.calculate_report_hourly",
        "schedule": crontab(minute=0, hour='*/1')
    },
    "run-every-day": {
        "task": "tasks.calculate_report_daily",
        "schedule": crontab(minute=0, hour=0)
    }
}
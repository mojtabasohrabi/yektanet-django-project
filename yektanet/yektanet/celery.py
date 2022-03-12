from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_task.settings')
app = Celery('celery_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

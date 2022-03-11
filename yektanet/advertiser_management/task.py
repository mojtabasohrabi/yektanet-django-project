from django.db.models.functions import TruncHour
from .models import Views, Clicks, DailyModel, HourlyModel, Ad
from datetime import datetime
from django.db.models import Count
from celery.schedules import crontab

from celery import Celery

app = Celery()


@app.task
def calculate_report_hourly():
    views = Views.objects.annotate(date=TruncHour('viewed_date')).values('date', 'ad') \
        .annotate(count=Count('ad')).values('ad', 'viewed_date', 'count').filter(
        viewed_date__hour=datetime.now().hour)
    clicks = Clicks.objects.annotate(date=TruncHour('clicked_date')).values('clicked_date', 'ad') \
        .annotate(count=Count('ad')).values('ad', 'clicked_date', 'count').filter(
        clicked_date__hour=datetime.now().hour)
    for ad in Ad.objects.values_list('pk'):
        HourlyModel.objects.create(ad_id=ad, clicks_count=clicks.get(ad_id=ad, default=0), date=datetime.now(),
                                   views_count=views.get(ad_id=ad),
                                   default=0)


@app.task
def calculate_report_daily():
    views = Views.objects.annotate(date=TruncHour('viewed_date')).values('date', 'ad').annotate(count=Count('ad')) \
        .values('ad', 'viewed_date', 'count').filter(
        viewed_date__hour=datetime.now().day)
    clicks = Clicks.objects.annotate(date=TruncHour('clicked_date')).values('clicked_date', 'ad').annotate(
        count=Count('ad')).values('ad', 'clicked_date', 'count').filter(
        clicked_date__hour=datetime.now().day)
    for ad in Ad.objects.values_list('pk'):
        DailyModel.objects.create(ad_id=ad, clicks=clicks.get(ad_id=ad, default=0), time=datetime.now(),
                                  views=views.get(ad_id=ad),
                                  default=0)


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

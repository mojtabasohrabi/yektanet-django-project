from django.db.models.functions import TruncHour
from .models import View, Click, ReportModel, Ad
from datetime import datetime
from django.db.models import Count

from celery import Celery

app = Celery()


@app.task
def calculate_report_hourly():
    views = View.objects.filter(
        viewed_date__hour=datetime.now().hour).annotate(date=TruncHour('created')).values('created', 'ad') \
        .annotate(count=Count('ad')).values('ad', 'created', 'count')
    clicks = Click.objects.filter(
        clicked_date__hour=datetime.now().hour).annotate(date=TruncHour('created')).values('created', 'ad') \
        .annotate(count=Count('ad')).values('ad', 'created', 'count')
    for ad in Ad.objects.values_list('pk'):
        ReportModel.objects.create(ad=ad, clicks_count=clicks.get(ad_id=ad, default=0),
                                   views_count=views.get(ad_id=ad),
                                   type_of_report='hourly')


@app.task
def calculate_report_daily():
    views = View.objects.filter(
        viewed_date__hour=datetime.now().day).values('created', 'ad').annotate(date=TruncHour('created')).annotate(count=Count('ad')) \
        .values('ad', 'created', 'count')
    clicks = Click.objects.filter(
        viewed_date__hour=datetime.now().day).values('created', 'ad').annotate(date=TruncHour('created')).annotate(
        count=Count('ad')).values('ad', 'created', 'count')
    for ad in Ad.objects.values_list('pk'):
        ReportModel.objects.create(ad=ad, clicks_count=clicks.get(ad_id=ad, default=0),
                                   views_count=views.get(ad_id=ad),
                                   type_of_report='daily')

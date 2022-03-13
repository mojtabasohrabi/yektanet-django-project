from django.db.models.functions import TruncHour
from .models import View, Click, ReportModel, Ad
from datetime import datetime
from django.db.models import Count

from celery import Celery

app = Celery()


@app.task
def calculate_report_hourly():
    views = View.objects.annotate(date=TruncHour('viewed_date')).values('date', 'ad') \
        .annotate(count=Count('ad')).values('ad', 'viewed_date', 'count').filter(
        viewed_date__hour=datetime.now().hour)
    clicks = Click.objects.annotate(date=TruncHour('clicked_date')).values('clicked_date', 'ad') \
        .annotate(count=Count('ad')).values('ad', 'clicked_date', 'count').filter(
        clicked_date__hour=datetime.now().hour)
    for ad in Ad.objects.values_list('pk'):
        ReportModel.objects.create(ad=ad, clicks_count=clicks.get(ad_id=ad, default=0),
                                   views_count=views.get(ad_id=ad),
                                   type_of_report='hourly')


@app.task
def calculate_report_daily():
    views = View.objects.annotate(date=TruncHour('viewed_date')).values('date', 'ad').annotate(count=Count('ad')) \
        .values('ad', 'viewed_date', 'count').filter(
        viewed_date__hour=datetime.now().day)
    clicks = Click.objects.annotate(date=TruncHour('clicked_date')).values('clicked_date', 'ad').annotate(
        count=Count('ad')).values('ad', 'clicked_date', 'count').filter(
        clicked_date__hour=datetime.now().day)
    for ad in Ad.objects.values_list('pk'):
        ReportModel.objects.create(ad=ad, clicks_count=clicks.get(ad_id=ad, default=0),
                                   views_count=views.get(ad_id=ad),
                                   type_of_report='daily')

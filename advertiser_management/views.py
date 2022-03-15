import random
from django.db.models import Count, Avg
from django.db.models.functions import TruncHour, TruncMinute
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ad, Advertiser, Click, View
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView, TemplateView
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class CreateAdFormView(CreateView):
    template_name = 'create_ad.html'
    model = Ad
    fields = ["advertiser", "title", "image", "link"]
    success_url = '/ads/'


class AdsView(APIView):

    def get(self, request, format=None):
        all_advertisers = Advertiser.objects.values('id', 'name')
        ads_fields = Ad.objects.values('id', 'image', 'advertiser', 'title')
        context = {
            'advertisers': all_advertisers,
            'ads': ads_fields,
        }

        return Response(context)


class ReportView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):

        all_clicks = Click.objects.annotate(hour=TruncHour('created')).values('ad', 'hour', 'user_ip').annotate(
            click=Count('*')).order_by('ad')

        all_views = View.objects.annotate(hour=TruncHour('created')).values('ad', 'hour', 'user_ip').annotate(
            view=Count('*')).order_by('ad')

        clicks = Click.objects.all()
        views = View.objects.all()
        time_difference = {}
        for click in clicks:
            time_difference[click.ad_id] = click.created - views.filter(ad=click.ad, user_ip=click.user_ip,
                                                                        created__lt=click.created) \
                .order_by('-created').first().created
        click_view_time_difference_average = time_difference

        ctr_per_ad = {}

        for i in all_views:
            ctr = {}
            for j in all_clicks:
                if i['ad'] == j['ad']:
                    readable_date = i['hour'].strftime("%Y/%m/%d, %H:%S")
                    ctr[readable_date] = j['click'] / i['view']
                    ctr_per_ad[i['ad']] = ctr

        context = {
            'click': all_clicks,
            'view': all_views,
            'ctr_per_ad': ctr_per_ad,
            'all_ads_time_difference_average': click_view_time_difference_average,
        }

        return Response(context)


class ClickView(RedirectView):
    pattern_name = 'click'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, id=kwargs['id'])
        return ad.link

import random
from django.db.models import Count
from django.db.models.functions import TruncHour, TruncMinute
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ad, Advertiser, Click, View
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView, TemplateView


class CreateAdFormView(CreateView):
    template_name = 'create_ad.html'
    model = Ad
    fields = ["advertiser", "title", "image", "link"]
    success_url = '/ads/'


class AdsView(TemplateView):
    template_name = "ads.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_advertisers = Advertiser.objects.values('id', 'name')
        ads_fields = Ad.objects.values('id', 'image', 'advertiser', 'title')
        for ad in ads_fields.iterator():
            View.insert_view(ad['id'], self.request.ip)

        context['advertisers'] = all_advertisers
        context['ads'] = ads_fields

        return context


class ReportView(TemplateView):
    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_clicks = Click.objects.annotate(hour=TruncHour('created')).values('ad', 'hour', 'user_ip').annotate(
            click=Count('*')).order_by('ad')

        all_views = View.objects.annotate(hour=TruncHour('created')).values('ad', 'hour', 'user_ip').annotate(
            view=Count('*')).order_by('ad')

        difference = {}
        clicks = Click.objects.all()
        views = View.objects.all()

        for click in clicks:
            ad_id = click.ad
            last_viewed_date = views.filter(ad_id=click.ad, user_ip=click.user_ip,
                                            created__lt=click.created) \
                .order_by('created').last().created
            difference[ad_id] = click.created - last_viewed_date

        all_ads_time_difference_average = difference

        ctr_per_ad = {}

        for i in all_views:
            ctr = {}
            for j in all_clicks:
                if i['ad'] == j['ad']:
                    readable_date = i['hour'].strftime("%Y/%m/%d, %H:%S")
                    ctr[readable_date] = j['click'] / i['view']
                    ctr_per_ad[i['ad']] = ctr

        context['click'] = all_clicks
        context['view'] = all_views
        context['ctr_per_ad'] = ctr_per_ad
        context['all_ads_time_difference_average'] = all_ads_time_difference_average

        return context


class ClickView(RedirectView):
    pattern_name = 'click'

    def get_redirect_url(self, *args, **kwargs):
        Click.insert_click(kwargs['id'], self.request.ip)
        ad = get_object_or_404(Ad, id=kwargs['id'])
        return ad.link

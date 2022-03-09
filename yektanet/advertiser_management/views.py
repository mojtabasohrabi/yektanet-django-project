from django.db.models import Count
from django.db.models.functions import TruncHour, TruncMinute
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import CrateAdForm
from django.shortcuts import redirect
from .models import Ad, Advertiser, Clicks, Views
from datetime import datetime


from django.views.generic.base import TemplateView


def redirect_view(url):
    response = redirect(url)
    return response


class AdsShow(TemplateView):
    template_name = "ads.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_advertisers = Advertiser.objects.values('id', 'name')
        ads_fields = Ad.objects.values('id', 'image', 'advertiser', 'title')
        all_ads = Ad.objects.all()
        for ad in all_ads.iterator():
            Views.insert_view(ad.id)
        context = {
            'advertisers': all_advertisers,
            'ads': ads_fields,
        }

        return context


class ReportShow(TemplateView):
    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_clicks = Clicks.objects.annotate(hour=TruncHour('clicked_date')).values('hour').annotate(
            click=Count('*')).values('ad', 'hour', 'click').order_by('ad')

        all_views = Views.objects.annotate(hour=TruncHour('viewed_date')).values('hour').annotate(
            view=Count('*')).values('ad', 'hour', 'view').order_by('ad')

        ctr_per_ad = {}
        for ad in Ad.objects.values('id'):
            ctr = {}
            for i in all_views:
                for j in all_clicks:
                    if ad['id'] == i['ad']:
                        readable_data = i['hour'].strftime("%Y/%m/%d, %H:%S")
                        ctr[readable_data] = j['click'] / i['view']
                        ctr_per_ad[i['ad']] = ctr

        context['click'] = all_clicks
        context['view'] = all_views
        context['ctr_per_ad'] = ctr_per_ad

        return context


def create_ad_show(request):
    if request.method == 'POST':
        form = CrateAdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ads/')
    else:
        form = CrateAdForm()

    return render(request, 'create_ad.html', {'form': form})


def click_show(request, id):
    Clicks.insert_click(id)
    return redirect(Ad.get_link(id))

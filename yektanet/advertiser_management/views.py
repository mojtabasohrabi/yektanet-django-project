from django.db.models import Count
from django.db.models.functions import TruncHour, TruncMinute
from .models import Ad, Advertiser, Clicks, Views
from django.views.generic.edit import CreateView

from django.views.generic.base import RedirectView, TemplateView
from django.shortcuts import redirect


class AdsView(TemplateView):
    template_name = "ads.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_advertisers = Advertiser.objects.values('id', 'name')
        ads_fields = Ad.objects.values('id', 'image', 'advertiser', 'title')
        all_ads = Ad.objects.all()
        for ad in all_ads.iterator():
            Views.insert_view(ad.id, self.request.ip)
        context = {
            'advertisers': all_advertisers,
            'ads': ads_fields,
        }

        return context


class CreateAdFormView(CreateView):
    template_name = 'create_ad.html'
    model = Ad
    fields = ["advertiser", "title", "image", "link"]
    success_url = '/ads/'


class ReportView(TemplateView):
    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_clicks = Clicks.objects.annotate(hour=TruncHour('clicked_date')).values('hour').annotate(
            click=Count('*')).values('ad', 'hour', 'click', 'user_ip').order_by('ad')

        all_views = Views.objects.annotate(hour=TruncHour('viewed_date')).values('hour').annotate(
            view=Count('*')).values('ad', 'hour', 'view', 'user_ip').order_by('ad')

        difference = {}
        clicks = Clicks.objects.all()
        views = Views.objects.all()
        for click in clicks:
            ad_id = click.ad
            difference[ad_id] = click.clicked_date - \
                                views.filter(ad_id=click.ad, user_ip=click.user_ip,
                                             viewed_date__lt=click.clicked_date) \
                                    .order_by('-viewed_date').first().viewed_date
        all_ads_time_difference_average = difference

        ctr_per_ad = {}
        for ad in Ad.objects.values('id'):
            ctr = {}
            for i in all_views:
                for j in all_clicks:
                    if ad['id'] == i['ad']:
                        readable_date = i['hour'].strftime("%Y/%m/%d, %H:%S")
                        ctr[readable_date] = j['click'] / i['view']
                        ctr_per_ad[i['ad']] = ctr

        context['click'] = all_clicks
        context['view'] = all_views
        context['ctr_per_ad'] = ctr_per_ad
        context['all_ads_time_difference_average'] = all_ads_time_difference_average

        return context


# def create_ad_show(request):
#     if request.method == 'POST':
#         form = CrateAdForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/ads/')
#     else:
#         form = CrateAdForm()
#
#     return render(request, 'create_ad.html', {'form': form})


def click_show(request, id):
    Clicks.insert_click(id, request.ip)
    return redirect(Ad.get_link(id))


# class ClickView(RedirectView):
#     pattern_name = 'click'
#
#     def get_redirect_url(self, *args, **kwargs):
#         ad = get_object_or_404(Ad, id=kwargs['id'])
#         return ad.link

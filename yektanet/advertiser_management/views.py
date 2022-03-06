from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import CrateAdForm
from django.shortcuts import redirect
from .models import Ad, Advertiser


def redirect_view(url):
    response = redirect(url)
    return response


# Create your views here.
def ads_show(request):
    all_advertisers = Advertiser.objects.values('id', 'name')
    ads_fields = Ad.objects.values('id', 'image', 'advertiser', 'title')
    all_ads = Ad.objects.all()
    for ad in all_ads.iterator():
        Ad.inc_views(ad.id)

    context = {
        'advertisers': all_advertisers,
        'ads': ads_fields,
    }
    return render(request, 'ads.html', context=context)


def create_ad_show(request):
    if request.method == 'POST':
        form = CrateAdForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ads/')
    else:
        form = CrateAdForm()

    return render(request, 'create_ad.html', {'form': form})


def click_show(request, id):
    Ad.inc_clicks(id)
    return redirect(Ad.get_link(id))

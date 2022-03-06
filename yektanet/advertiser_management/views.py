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
    all_ads = Ad.objects.values('id', 'image', 'advertiser', 'title')

    context = {
        'advertisers': all_advertisers,
        'ads': all_ads,
    }
    return render(request, 'ads.html', context=context)


def create_ad_show(request):
    if request.method == 'POST':
        form = CrateAdForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            return HttpResponseRedirect('/ads/')
    else:
        form = CrateAdForm()

    return render(request, 'create_ad.html', {'form': form})


def click_show(request, id):
    return redirect(Ad.get_link(id))

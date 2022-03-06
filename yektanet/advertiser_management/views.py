from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import CrateAdForm


# Create your views here.
def ads_show(request):
    return render(request, "ads.html")


def create_ad_show(request):
    if request.method == 'POST':
        form = CrateAdForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/ads.html/')
    else:
        form = CrateAdForm()

    return render(request, 'create_ad.html', {'form': form})


def click_show(request):
    return render(request, "click.html")

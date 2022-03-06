from django.urls import path
from . import views

urlpatterns = [
    path('ads/', views.ads_show, name='ads'),
    path('create_ad/', views.create_ad_show, name='create_ad'),
    path('click/', views.click_show, name='click'),
]

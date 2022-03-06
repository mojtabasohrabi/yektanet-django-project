from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ads/', views.ads_show, name='ads'),
    path('create_ad/', views.create_ad_show, name='create_ad'),
    path('click/<int:id>/', views.click_show, name='click'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

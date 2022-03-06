from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AdsShow, ReportShow

urlpatterns = [
    path('ads/', AdsShow.as_view(), name='ads'),
    path('create_ad/', views.create_ad_show, name='create_ad'),
    path('click/<int:id>/', views.click_show, name='click'),
    path('report/', ReportShow.as_view(), name='report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

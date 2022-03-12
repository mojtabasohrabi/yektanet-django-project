from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AdsView, ReportView, ClickView, CreateAdFormView

urlpatterns = [
    path('ads/', AdsView.as_view(), name='ads'),
    path('create_ad/', CreateAdFormView.as_view(), name='create_ad'),
    path('click/<int:id>/', ClickView.as_view(), name='click'),
    path('report/', ReportView.as_view(), name='report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from .models import Ad
from .models import Advertiser


@admin.register(Ad)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Advertiser)
class PersonAdmin(admin.ModelAdmin):
    pass

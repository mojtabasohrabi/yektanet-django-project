from django.contrib import admin
from .models import Ad
from .models import Advertiser

from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("title", "approve")
    list_filter = ("title", "approve")
    list_editable = ["approve"]
    search_fields = ['title']


admin.site.register(Ad, ProfileAdmin)


# @admin.register(Ad)
# class PersonAdmin(admin.ModelAdmin):
#     pass


@admin.register(Advertiser)
class PersonAdmin(admin.ModelAdmin):
    pass

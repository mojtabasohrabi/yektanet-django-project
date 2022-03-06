from django.forms import ModelForm
from .models import Ad


class CrateAdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ["advertiser", "title", "image", "link"]

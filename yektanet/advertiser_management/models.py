from django.db import models
from django.db.models import Count
from django.utils import timezone


class Advertiser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    image = models.ImageField(default='')
    link = models.TextField()
    approve = models.BooleanField(default=False)

    @staticmethod
    def get_link(ad_id):
        ad = Ad.objects.get(id=ad_id)
        link = ad.link
        return link


class Clicks(models.Model):
    id = models.AutoField(primary_key=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    clicked_date = models.DateTimeField()
    user_ip = models.CharField(max_length=15)

    def insert_click(ad_id):
        ad = Ad.objects.get(id=ad_id)
        data_to_insert = Clicks(ad=ad, clicked_date=timezone.now(), user_ip='')
        data_to_insert.save(force_insert=True)


class Views(models.Model):
    id = models.AutoField(primary_key=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    viewed_date = models.DateTimeField()
    user_ip = models.CharField(max_length=15)

    def insert_view(ad_id):
        ad = Ad.objects.get(id=ad_id)
        data_to_insert = Views(ad=ad, viewed_date=timezone.now(), user_ip='')
        data_to_insert.save(force_insert=True)

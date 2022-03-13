from django.db import models
from django.db.models import Count
from django.utils import timezone


class Advertiser(models.Model):
    name = models.CharField(max_length=200)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ads_images')
    link = models.CharField(max_length=255)
    approve = models.BooleanField(default=False)

    @staticmethod
    def get_link(ad_id):
        ad = Ad.objects.get(id=ad_id)
        link = ad.link
        return link


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(protocol='IPv4')

    @staticmethod
    def insert_click(ad_id, user_ip):
        ad = Ad.objects.get(id=ad_id)
        data_to_insert = Click(ad=ad, user_ip=user_ip)
        data_to_insert.save(force_insert=True)


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(protocol='IPv4')

    @staticmethod
    def insert_view(ad_id, user_ip):
        ad = Ad.objects.get(id=ad_id)
        data_to_insert = View(ad=ad, user_ip=user_ip)
        data_to_insert.save(force_insert=True)


class ReportModel(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField()
    clicks_count = models.PositiveIntegerField()
    type_of_report = models.CharField(max_length=10)

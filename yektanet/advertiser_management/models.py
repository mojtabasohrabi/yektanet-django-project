from django.db import models


class Advertiser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    #advertiser_id = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image_url = models.CharField(max_length=255)
    link = models.TextField()
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    approve = models.BooleanField(default=False)
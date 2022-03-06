from django.db import models


class Advertiser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(default='')
    link = models.TextField()
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    approve = models.BooleanField(default=False)

    @staticmethod
    def get_link(ad_id):
        ad = Ad.objects.get(id=ad_id)
        link = ad.link
        return link

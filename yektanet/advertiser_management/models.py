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
    approve = models.BooleanField(default=False)

    @staticmethod
    def get_link(ad_id):
        ad = Ad.objects.get(id=ad_id)
        link = ad.link
        return link

    def inc_clicks(ad_id):
        t = Ad.objects.get(id=ad_id)
        t.clicks += 1  # change field
        t.save()  # this will update only

    def inc_views(ad_id):
        t = Ad.objects.get(id=ad_id)
        t.views += 1  # change field
        t.save()  # this will update only


class Clicks(models.Model):
    id = models.AutoField(primary_key=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    clicked_date = models.DateTimeField()
    user_ip = models.CharField(max_length=15)


class Views(models.Model):
    id = models.AutoField(primary_key=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    viewed_date = models.DateTimeField()
    user_ip = models.CharField(max_length=15)
from datetime import datetime  # datetime of machine
from django.utils import timezone  # django timezone
from django.conf import settings

from django.db import models


# Create your models here.

class MarketingQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True) \
            .filter(start_date__lte=timezone.now()) \
            .filter(end_date__gte=timezone.now())
        # .filter(start_date__lte=datetime.now()) \
        # .filter(end_date__gte=datetime.now())


class MarketingManager(models.Manager):
    def get_queryset(self):
        return MarketingQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def all_featured(self):
        return self.get_queryset().active().featured()

    def get_featured_item(self):
        try:
            return self.get_queryset().active().featured()[0]  # new one first
        except:
            return None


class MarketingMessage(models.Model):
    message = models.CharField(max_length=120)
    active = models.BooleanField(default=False)  # actually show up
    featured = models.BooleanField(default=False)  # featurning right now
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = MarketingManager()

    def __str__(self):
        return str(self.message[:12])

    class Meta:
        ordering = ['-start_date', '-end_date']  # stack


def slider_upload(instance, filename):
    return "images/marketing/slider/%s" % (filename)


class Slider(models.Model):
    image = models.ImageField(upload_to=slider_upload)  # filefield can also be used
    order = models.IntegerField(default=0)
    url_link = models.CharField(max_length=150, null=True, blank=True)
    headertext = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)  # actually show up
    featured = models.BooleanField(default=False)  # featurning right now
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = MarketingManager()

    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['order','-start_date', '-end_date']  # stack

    def get_image_url(self):
        #print("http://127.0.0.1:8000%s%s" % (settings.MEDIA_URL, self.image))
        return "http://127.0.0.1:8000%s%s" % (settings.MEDIA_URL, self.image)

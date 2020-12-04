from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from irrigation.settings import *


# Create your models here.
class Setting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notification = models.BooleanField('Notifiche email', default=True)


class Location(models.Model):
    city = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.city


class Garden(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    last_rain = models.DateTimeField('ultima pioggia', blank=True, null=True)
    next_rain = models.DateTimeField(default='2012-01-01 00:01')
    temperature = models.FloatField(blank=True, null=True)
    image = models.CharField(max_length=255,
                             choices=IMG_CHOICES,
                             default=PLANT)
    ip = models.CharField('Indirizzo Ip Esp32', max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Area(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=10)
    humidity = models.IntegerField(default=0)
    last_irrigation = models.DateTimeField('Ultima irrigazione', default="2012-01-01 00:01", editable=False)
    irrigation_type = models.CharField(max_length=1, choices=IRRIGATION, default=MANUAL)
    relay = models.IntegerField('Interruttore', blank=True, null=True)

    def __str__(self):
        return self.name

    def was_irrigated_recently(self):
        return self.last_irrigation >= timezone.now() - datetime.timedelta(days=1)


class Irrigation(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    date = models.DateField('data di irrigazione', default=timezone.now)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    irrigation_type = models.CharField(max_length=1, choices=IRRIGATION, default=MANUAL)

    def get_duration(self):
        delta = self.end - self.start
        return divmod(delta.total_seconds(), 60)[0]

    def __str__(self):
        return str(self.date)


class ScheduledIrrigation(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, default=None)
    frequency = models.CharField('frequenza', max_length=10, choices=FREQUENCY, default='2')
    duration = models.CharField('durata', max_length=100, choices=zip(DURATION, DURATION), default='20 minuti')
    hour = models.TimeField('Orario', default=datetime.time(00, 00))


class Rain(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, default=None)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(blank=True, null=True)

    def get_duration(self):
        if self.end is not None:
            delta = self.end - self.start
            return divmod(delta.total_seconds(), 60)[0]
        else:
            return None

    def __str__(self):
        return str(self.start)

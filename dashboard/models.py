from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

PLANT = 'cover/balcony.jpg'
TERRACE = 'cover/terrace.jpg'
FLOWER = 'cover/flower.jpg'
GARDEN = 'cover/garden.jpg'
VEGETABLE = 'cover/vegetable.jpg'
IMG_CHOICES = (
    (PLANT, 'Pianta'),
    (TERRACE, 'Albero'),
    (GARDEN, 'Prato'),
    (VEGETABLE, 'Verdura'),
    (FLOWER, 'Fiore'),

)

MANUAL = 'M'
CALENDAR = 'C'
SMART = 'S'
IRRIGATION = [
    (MANUAL, 'Manuale'),
    (CALENDAR, 'Calendario'),
    (SMART, 'Intelligente'),
]


# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.city


class Garden(models.Model):
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    city = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    last_rain = models.DateTimeField('date of last_rain', default="2012-01-01 00:01", editable=False)
    next_rain = models.DateTimeField(default=datetime.date.today())
    image = models.CharField(max_length=255,
                             choices=IMG_CHOICES,
                             default=PLANT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Area(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    last_irrigation = models.DateTimeField('date of irrigation', default="2012-01-01 00:01", editable=False)
    irrigation_type = models.CharField(max_length=1, choices=IRRIGATION, default=MANUAL)

    def __str__(self):
        return self.name

    def was_irrigated_recently(self):
        return self.last_irrigation >= timezone.now() - datetime.timedelta(days=1)


class Irrigation(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, default=None)
    irrigation = models.DateField('date of irrigation')
    start = models.TimeField()
    end = models.TimeField()
    irrigation_type = models.CharField(max_length=1, choices=IRRIGATION, default=MANUAL)

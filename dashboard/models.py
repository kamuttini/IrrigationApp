from django.db import models
import datetime
from django.utils import timezone

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
    city = models.ForeignKey( Location , on_delete=models.CASCADE, default=None)
    last_rain = models.DateTimeField('date of last_rain', default=None)

    def __str__(self):
        return self.name

class Area(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    last_irrigation = models.DateTimeField('date of irrigation')

    def __str__(self):
        return self.name

    def was_irrigated_recently(self):
        return self.last_irrigation >= timezone.now() - datetime.timedelta(days=1)




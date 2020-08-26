from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Garden(models.Model):
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)

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

class Location(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, default=None)
    city = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.city

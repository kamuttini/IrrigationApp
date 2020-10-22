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
    (CALENDAR, 'Programmata'),
    (SMART, 'Intelligente'),
]

FREQUENCY = [
    ('0', 'ogni giorno'),
    ('1', 'giorni alterni'),
    ('2', 'ogni 2 giorni'),
    ('3', 'ogni 3 giorni'),
    ('4', 'ogni 4 giorni'),
    ('5', 'ogni 5 giorni'),
    ('7', 'una volta a settimana'),
    ('10', 'ogni 10 giorni'),
    ('14', 'una volta ogni due settimane'),
]

DURATION = [
    '1 minuto ', '2 minuti ', '3 minuti ', '4 minuti ', '5 minuti ', '6 minuti ', '7 minuti ', '8 minuti ', '9 minuti ',
    '10 minuti ', '11 minuti ', '12 minuti ', '13 minuti ', '14 minuti ', '15 minuti ', '20 minuti ', '25 minuti ',
    '30 minuti ', '40 minuti ', '30 minuti ', '45 minuti ',
    '50 minuti ', '55 minuti ', '60 minuti ',
]


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
    position = models.IntegerField(default=0)
    city = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    last_rain = models.DateTimeField('ultima pioggia', default="2012-01-01 00:01", editable=False)
    next_rain = models.DateTimeField(default='2012-01-01 00:01')
    image = models.CharField(max_length=255,
                             choices=IMG_CHOICES,
                             default=PLANT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Area(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=10)
    position = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    last_irrigation = models.DateTimeField('ultima irrigazione', default="2012-01-01 00:01", editable=False)
    irrigation_type = models.CharField(max_length=1, choices=IRRIGATION, default=MANUAL)

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

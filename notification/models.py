import django.utils
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from dashboard.models import Area


# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user=kwargs.get('instance'),
                                    title="Benvenuto nella Dashboard",
                                    message="Grazie per esserti registrato")

@receiver(pre_save, sender=Area)
def notify_low_humidity(sender, instance, **kwargs):
    if instance.humidity < 30:
        message = f"l'umidità della zona {instance} è sotto il 30%."
        Notification.objects.create(user=instance.garden.user,
                                    title="Umidità bassa",
                                    message= message)

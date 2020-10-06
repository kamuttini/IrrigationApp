import django.utils
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from dashboard.models import Area, Setting, Irrigation
from django.core.mail import send_mail


# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def initial_settings(sender, **kwargs):
    if kwargs.get('created', False):
        Setting.objects.create(user=kwargs.get('instance')),
        Notification.objects.create(user=kwargs.get('instance'),
                                    title="Benvenuto nella Dashboard",
                                    message="Grazie per esserti registrato")
        Notification.objects.create(user=kwargs.get('instance'),
                                    title="Notifiche email",
                                    message="Le notifiche via email sono attive di default. Puoi modificare queste scelta in Imostazioni")

@receiver(post_save, sender=Irrigation)
def initial_settings(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user=instance.area.garden.user,
                                    title="Irrigazione manuale avviata",
                                    message=f'zona: {instance.area}')


@receiver(pre_save, sender=Area)
def notify_low_humidity(sender, instance, **kwargs):
    if instance.humidity < 30:
        message = f"l'umidità della zona {instance} è sotto il 30%."
        settings = get_object_or_404(Setting, user=instance.garden.user)
        if settings.email_notification:
            send_mail(
                f'Umidità della zona {instance} bassa',
                'umidità sotto il 30%, intervenire',
                'camilla.cantiani@gmail.com',
                [instance.garden.user.email],
                fail_silently=False,
            )
        Notification.objects.create(user=instance.garden.user,
                                    title="Umidità bassa",
                                    message=message)

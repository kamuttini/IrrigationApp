from datetime import datetime

import django.utils
import requests
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from dashboard.models import Area, Setting, Irrigation, ScheduledIrrigation
from django.core.mail import send_mail
from django_celery_beat.models import IntervalSchedule, PeriodicTask


# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def initial_settings(sender, **kwargs):
    if kwargs.get('created', False):
        Setting.objects.create(user=kwargs.get('instance')),
        Notification.objects.create(user=kwargs.get('instance'),
                                    title="Benvenuto nella Dashboard",
                                    message="Grazie per esserti registrato")
        Notification.objects.create(user=kwargs.get('instance'),
                                    title="Notifiche email",
                                    message="Le notifiche via email sono attive di default. Puoi modificare queste scelta in Impostazioni")


@receiver(post_save, sender=Irrigation)
def irrigation(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # create notification
        Notification.objects.create(user=instance.area.garden.user,
                                    title="Irrigazione manuale avviata",
                                    message=f'zona: {instance.area}')

        # update last irrigation field of current area
        area = get_object_or_404(Area, pk=instance.area.pk)
        area.last_irrigation = instance.date
        area.save()


@receiver(pre_save, sender=Area)
def notify_low_humidity(sender, instance, **kwargs):
    if instance.humidity < 30:
        message = f"l'umidità della zona {instance} è sotto il 30%."
        settings = get_object_or_404(Setting, user=instance.garden.user)
        if settings.email_notification:
            send_mail(
                f'Umidità della zona {instance} bassa',
                'umidità sotto il 30%, intervenire',
                'irrigator.it@gmail.com',
                [instance.garden.user.email],
                fail_silently=False,
            )
        Notification.objects.create(user=instance.garden.user,
                                    title="Umidità bassa",
                                    message=message)


@receiver(post_save, sender=ScheduledIrrigation)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if not created and instance.area.irrigation_type == 'C':
        start_time: datetime = datetime.today()
        start_time.replace(int(str(datetime.today().year)), int(str(datetime.today().month)),
                           int(str(datetime.today().day)), int(str(instance.hour.hour)))
        PeriodicTask.objects.create(name='on_' + str(instance.area),
                                    task='relay_on',
                                    enabled=True,
                                    interval=IntervalSchedule.objects.get(every=instance.frequency, period='days'),
                                    args=[instance.area.garden.ip, instance.area.relay],
                                    start_time=start_time)

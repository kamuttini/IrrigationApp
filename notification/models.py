import json
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
        task_name_on = 'on_' + str(instance.area.id)
        task_name_off = 'off_' + str(instance.area.id)
        if PeriodicTask.objects.filter(name=task_name_on).exists():
            get_object_or_404(PeriodicTask, name=task_name_on).delete()

        if PeriodicTask.objects.filter(name=task_name_off).exists():
            get_object_or_404(PeriodicTask, name=task_name_off).delete()

        PeriodicTask.objects.create(name=task_name_on,
                                    task='irrigation.celery.relay_on',
                                    enabled=True,
                                    interval=IntervalSchedule.objects.get(every='15', period='seconds'),
                                    kwargs=json.dumps({"ip": instance.area.garden.ip, "relay": instance.area.relay, "area": instance.area.pk, "duration": instance.duration}))

        PeriodicTask.objects.create(name=task_name_off,
                                    task='irrigation.celery.relay_off',
                                    enabled=True,
                                    interval=IntervalSchedule.objects.get(every='25', period='seconds'),
                                    kwargs=json.dumps({"ip": instance.area.garden.ip, "relay": instance.area.relay}))



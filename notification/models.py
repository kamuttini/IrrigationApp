import json

import django.utils
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from dashboard.models import Area, Setting, Irrigation, ScheduledIrrigation
from django.core.mail import send_mail
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
import datetime as DT


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


@receiver(pre_save, sender=Area)
def check_irrigation_type(sender, instance, **kwargs):
    task_name_on = 'on_' + str(instance.id)
    task_name_off = 'off_' + str(instance.id)
    if instance.irrigation_type == 'M' or instance.irrigation_type == 'S':
        if PeriodicTask.objects.filter(name=task_name_on).exists():
            get_object_or_404(PeriodicTask, name=task_name_on).delete()

        if PeriodicTask.objects.filter(name=task_name_off).exists():
            get_object_or_404(PeriodicTask, name=task_name_off).delete()


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
                                    crontab=start_frequency(instance.frequency, instance.hour),
                                    kwargs=json.dumps({"ip": instance.area.garden.ip, "relay": instance.area.relay,
                                                       "area": instance.area.pk, "duration": instance.duration}))

        PeriodicTask.objects.create(name=task_name_off,
                                    task='irrigation.celery.relay_off',
                                    enabled=True,
                                    crontab=stop_frequency(instance.frequency, instance.hour, instance.duration),
                                    kwargs=json.dumps({"ip": instance.area.garden.ip, "relay": instance.area.relay}))


# function that returns the frequency value for crontab jobs
def start_frequency(drange, hour):
    today = DT.date.today().day
    if drange == 2:
        if today % 2 == 0:
            if not CrontabSchedule.objects.filter(minute='0', hour=hour, day_of_month='2-30/2').exists():
                obj = CrontabSchedule.objects.create(minute='0', hour=hour, day_of_month='2-30/2')
            else:
                obj = get_object_or_404(CrontabSchedule, minute='0', hour=hour, day_of_month='2-30/2')

        else:
            if not CrontabSchedule.objects.filter(minute='0', hour=hour, day_of_month='1-30/2').exists():
                obj = CrontabSchedule.objects.create(minute='0', hour=hour, day_of_month='1-30/2')
            else:
                obj = get_object_or_404(CrontabSchedule, minute='0', hour=hour, day_of_month='1-30/2')

    else:
        repetition = '*/' + drange
        if not CrontabSchedule.objects.filter(minute='0', hour=hour, day_of_month=repetition).exists():
            obj = CrontabSchedule.objects.create(minute='0', hour=hour, day_of_month=repetition)
        else:
            obj = get_object_or_404(CrontabSchedule, minute='0', hour=hour, day_of_month=repetition)
    return obj


def stop_frequency(drange, hour, min):
    today = DT.date.today().day
    if min == '60':
        min = '59'

    today = DT.date.today().day
    if drange == 2:
        if today % 2 == 0:
            if not CrontabSchedule.objects.filter(minute=min, hour=hour, day_of_month='2-30/2').exists():
                obj = CrontabSchedule.objects.create(minute=min, hour=hour, day_of_month='2-30/2')
            else:
                obj = get_object_or_404(CrontabSchedule, minute=min, hour=hour, day_of_month='2-30/2')

        else:
            if not CrontabSchedule.objects.filter(minute=min, hour=hour, day_of_month='1-30/2').exists():
                obj = CrontabSchedule.objects.create(minute=min, hour=hour, day_of_month='1-30/2')
            else:
                obj = get_object_or_404(CrontabSchedule, minute=min, hour=hour, day_of_month='1-30/2')

    else:
        repetition = '*/' + drange
        if not CrontabSchedule.objects.filter(minute=min, hour=hour, day_of_month=repetition).exists():
            obj = CrontabSchedule.objects.create(minute=min, hour=hour, day_of_month=repetition)
        else:
            obj = get_object_or_404(CrontabSchedule, minute=min, hour=hour, day_of_month=repetition)
    return obj

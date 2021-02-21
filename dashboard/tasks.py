import json

import requests
from celery import shared_task
from django.shortcuts import get_object_or_404
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule, ClockedSchedule
import datetime as DT
from dashboard.methods import is_raining,has_rained, get_rain_probability, start_frequency, stop_frequency
from dashboard.models import ScheduledIrrigation


@shared_task
def relay_on(ip, relay, area, duration):
    requests.request('POST', 'http://raspberry/register_irrigation/C/' + str(area) + '/' + duration + '/')

    # call to relay
    server_url = 'http://' + str(ip)
    url = server_url + '/update?relay=' + str(relay) + '&state=1'
    requests.request('GET', url)


@shared_task
def relay_off(ip, relay):
    # call to relay
    server_url = 'http://' + str(ip)
    url = server_url + '/update?relay=' + str(relay) + '&state=0'
    requests.request('GET', url)


@shared_task
def next_smart_event(ip, relay, area, duration):
    today = DT.date.today()
    task_name_on = 'on_' + str(area.id)
    task_name_off = 'off_' + str(area.id)
    scheduled_irrigation = get_object_or_404(ScheduledIrrigation, area=area)

    # se sta piovendo o ha piovuto nelle ultime 12 ore salta l'irrigazione prevista e crea uno nuovo smart_event per la prossima
    if is_raining() or has_rained():
        PeriodicTask.objects.create(name=task_name_on,
                                    task='irrigation.celery.next_smart_evemt',
                                    enabled=True,
                                    crontab=start_frequency(scheduled_irrigation.frequency, scheduled_irrigation.hour),
                                    kwargs=json.dumps({"ip": area.garden.ip, "relay": area.relay,
                                                       "area": area.pk, "duration": scheduled_irrigation.duration}))

        PeriodicTask.objects.create(name=task_name_off,
                                    task='irrigation.celery.relay_off',
                                    enabled=True,
                                    crontab=stop_frequency(1, scheduled_irrigation.hour,
                                                           scheduled_irrigation.duration),
                                    one_off=True,
                                    kwargs=json.dumps({"ip": area.garden.ip, "relay": area.relay}))

    # se per oggi è prevista pioggia, rimanda l'irrrigazione alla sera
    elif get_rain_probability(area, 'today'):
        next_event = today + DT.timedelta(hours=12)
        obj = ClockedSchedule.objects.create(date=next_event)
        PeriodicTask.objects.create(name=task_name_on,
                                    task='irrigation.celery.next_smart_evemt',
                                    enabled=True,
                                    clocked_schedule=obj,
                                    kwargs=json.dumps({"ip": area.garden.ip, "relay": area.relay,
                                                       "area": area.pk, "duration": scheduled_irrigation.duration}))

    # se è prevista pioggia per domani riduce il tempo dell'irrigazione anticipando la task relay_off (dimezza il valore)
    elif get_rain_probability(area, 'tomorrow'):
        PeriodicTask.objects.create(name=task_name_off,
                                    task='irrigation.celery.relay_off',
                                    enabled=True,
                                    crontab=stop_frequency(1, scheduled_irrigation.hour,
                                                           int(scheduled_irrigation.duration) / 2),
                                    one_off=True,
                                    kwargs=json.dumps({"ip": area.garden.ip, "relay": area.relay}))
        # irriga
        relay_on()

    #se nessuno dei casi precedenti irriga normalmente
    else:
        PeriodicTask.objects.create(name=task_name_off,
                                    task='irrigation.celery.relay_off',
                                    enabled=True,
                                    crontab=stop_frequency(1, scheduled_irrigation.hour,
                                                           int(scheduled_irrigation.duration)),
                                    one_off=True,
                                    kwargs=json.dumps({"ip": area.garden.ip, "relay": area.relay}))
        relay_on()
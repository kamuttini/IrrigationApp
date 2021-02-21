from django.shortcuts import get_object_or_404
from django_celery_beat.models import CrontabSchedule

from static.translation import WEATHER, WEEK
import requests
import datetime as DT
from .models import Area, Garden, Rain, Location
from django.db.models import Q
from mysettings import WEATHER_API_KEY


def get_weather_info(location, forecast_type):
    today = DT.date.today()

    url = "https://api.climacell.co/v3/weather/forecast/" + forecast_type

    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability,temp,weather_code",
                   "apikey": WEATHER_API_KEY}

    response = requests.request("GET", url, params=querystring).json()
    weather_info = []

    if forecast_type == "daily":
        for i in range(5):
            day_of_week = today + DT.timedelta(days=i)
            info_day = {
                'day': WEEK[day_of_week.strftime("%a")],

                'temperature_min': float(response[i]['temp'][0]['min']['value'])
                ,
                'temperature_max': float(response[i]['temp'][1]['max']['value'])
                ,
                'precipitation': str(response[i]['precipitation_probability']['value']) +
                                 response[i]['precipitation_probability']['units'],
                'description': response[i]['weather_code']['value']
            }

            weather_icons_path = "images/weather icons/color/" + info_day['description'] + ".svg"

            info_day['description'] = (WEATHER[info_day['description']])
            weather_info.append([info_day, weather_icons_path])
        context = {
            'weather_info': weather_info
        }

    else:
        info_day = {
            'day': WEEK[today.strftime("%a")],
            'temp': str(response[0]['temp']['value']) + '°' + response[0]['temp']['units'],
            'precipitation': str(response[0]['precipitation_probability']['value']),
            'description': response[0]['weather_code']['value'],
            'weather_icons_path': ""
        }
        info_day['weather_icons_path'] = "images/weather icons/color/" + info_day['description'] + ".svg"
        info_day['description'] = (WEATHER[info_day['description']])
        context = info_day

    return context


def get_rain(location, mode):
    url = "https://api.climacell.co/v3/weather/forecast/daily"

    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability",
                   "apikey": WEATHER_API_KEY}

    response = requests.request("GET", url, params=querystring).json()

    if mode == 'next':
        weather_info = []
        for i in range(15):
            info_day = {
                'location': location,
                'date': response[i]['observation_time']['value'],
                'precipitation': str(response[i]['precipitation_probability']['value']),
            }
            weather_info.append(info_day)

        context = "più di 12"
        for item in weather_info:
            if item['precipitation'] >= "50":
                return weather_info.index(item)

    return context


def search(request):
    query = request.GET.get('q')
    queries = query.split(" ")
    qs = Area.objects.filter(garden__user=request.user)
    qs2 = Garden.objects.filter(user=request.user)
    if query is not None:
        for item in queries:
            qs = qs.filter(
                Q(name__icontains=item) |
                Q(garden__city__city__icontains=item))

            qs2 = qs2.filter(
                Q(name__icontains=item) |
                Q(city__city__icontains=item))

    return qs, qs2


def activate_relay(ip, relay):
    # call to activate relay
    server_url = 'http://' + str(ip)
    url = server_url + '/update?relay=' + str(relay) + '&state=1'
    requests.request('GET', url)


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


def is_raining(area):
    today = DT.date.today().day
    if Rain.objects.exists(garden=area.garden, start=today, end=None):
        return True
    return False


def get_rain_probability(area, day):
    url = "https://api.climacell.co/v3/weather/forecast/daily"
    location = get_object_or_404(Location, city=area.garden.city)
    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability",
                   "apikey": WEATHER_API_KEY}

    response = requests.request("GET", url, params=querystring).json()

    if day == 'today':
        i = 0
    else:
        i = 1
    if response[i]['precipitation_probability']['value'] >= 50:
        return True

    return False


def has_rained(area):
    today = DT.date.today()
    ref = today-DT.timedelta(hours=12)
    if Rain.objects.exists(garden=area.garden, start__gte=ref):
        return True

    return False

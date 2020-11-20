from static.translation import WEATHER, WEEK
import requests
import datetime as DT
from .models import Area, Garden
from django.db.models import Q
from secrets import WEATHER_API_KEY

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

    if forecast_type == "hourly":
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
                   "apikey": "6KIHRzYEnmDjo2nD68e6GWlHYGfbRIO2"}

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
    elif mode == 'today':
        info_day = {
            'location': location,
            'date': response[0]['observation_time']['value'],
            'precipitation': str(response[0]['precipitation_probability']['value']),
        }
        context = info_day
    elif mode == 'tomorrow':
        info_day = {
            'location': location,
            'date': response[1]['observation_time']['value'],
            'precipitation': str(response[1]['precipitation_probability']['value']),
        }
        context = info_day
    return context


def irrigate(location, umidity):
    time = DT.time
    irrigation = False
    rain_tod = get_rain(location, 'today')
    rain_tom = get_rain(location, 'tomorrow')

    if time.hour == 6:
        if rain_tom['precipitation'] > 50 and umidity < 30:
            print("Irrigazione minore effettuata")  # IRRIGA DI MENO
            irrigation = True
        if not irrigation and (umidity < 30 or rain_tod['precipitation'] < 50):
            print("Irrigazione effettuata")  # IRRIGA
            irrigation = True

    if not irrigation and time.hour == 20:
        if rain_tom['precipitation'] > 50 and umidity < 30:
            print("Irrigazione minore effettuata")  # IRRIGA DI MENO
            irrigation = True
        if not irrigation and (umidity < 30 or rain_tod['precipitation'] < 50):
            print("Irrigazione effettuata")  # IRRIGA
            irrigation = True

    return irrigation


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

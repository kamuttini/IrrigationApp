from .static.translation import WEATHER, WEEK
import requests
import datetime as DT


def get_weather_info(location, forecast_type):
    today = DT.date.today()

    url = "https://api.climacell.co/v3/weather/forecast/" + forecast_type

    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability,temp,weather_code",
                   "apikey": "6KIHRzYEnmDjo2nD68e6GWlHYGfbRIO2"}

    response = requests.request("GET", url, params=querystring).json()
    weather_info = []

    if forecast_type == "daily":
        for i in range(5):
            day_of_week = today + DT.timedelta(days=i)
            info_day = {
                'day': WEEK[day_of_week.strftime("%a")],

                'temperature_min': str(response[i]['temp'][0]['min']['value']) + '°' +
                                   response[i]['temp'][0]['min'][
                                       'units'],
                'temperature_max': str(response[i]['temp'][1]['max']['value']) + '°' +
                                   response[i]['temp'][1]['max'][
                                       'units'],
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


def get_next_rain(location):
    url = "https://api.climacell.co/v3/weather/forecast/daily"

    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability",
                   "apikey": "ncVu9PBL8D7vTbPbY3NKJRRbtQ0yAX1S"}

    response = requests.request("GET", url, params=querystring).json()

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

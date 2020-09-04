from .static.translation import WEATHER
import requests
import datetime as DT


def get_weather_info(location, day):
    url = "https://api.climacell.co/v3/weather/forecast/daily"
    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability,temp,weather_code",
                   "apikey": "6KIHRzYEnmDjo2nD68e6GWlHYGfbRIO2"}

    response = requests.request("GET", url, params=querystring).json()"""
    today = DT.date.today()
    day_of_week = today + DT.timedelta(days=day)

    weather_info = {
        'day': day_of_week.strftime("%a"),
        'temperature_min': str(response[day]['temp'][0]['min']['value']) + '°' + response[day]['temp'][0]['min'][
            'units'],
        'temperature_max': str(response[day]['temp'][1]['max']['value']) + '°' + response[day]['temp'][1]['max'][
            'units'],
        'precipitation': str(response[day]['precipitation_probability']['value']) +
                         response[day]['precipitation_probability']['units'],
        'description': response[day]['weather_code']['value']
    }

    image_icon = weather_info['description'] + ".svg"
    weather_icons_path = "images/weather icons/color/" + image_icon

    # translation
    weather_info['description'] = (WEATHER[weather_info['description']])

    context = {
        'weather_info': weather_info,
        'icon_path': weather_icons_path
    }
    return context"""
    context = {
        'weather_info' : weather_info
    }

    return context
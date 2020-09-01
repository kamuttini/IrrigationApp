from .static.translation import WEATHER
import requests


def get_weather_info(location):
    url = "https://api.climacell.co/v3/weather/forecast/daily"
    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability,temp,weather_code",
                   "apikey": "6KIHRzYEnmDjo2nD68e6GWlHYGfbRIO2"}

    response = requests.request("GET", url, params=querystring).json()

    weather_info = {
        'location': location,
        'temperature_min': str(response[0]['temp'][0]['min']['value']) + '° ' + response[0]['temp'][0]['min']['units'],
        'temperature_max': str(response[0]['temp'][1]['max']['value']) + '° ' + response[0]['temp'][1]['max']['units'],
        'precipitation': str(response[0]['precipitation_probability']['value']) +
                         response[0]['precipitation_probability']['units'],
        'description': response[0]['weather_code']['value']
    }

    image_icon = weather_info['description'] + ".svg"
    weather_icons_path = "images/weather icons/color/" + image_icon

    # translation
    weather_info['description'] = (WEATHER[weather_info['description']])

    context = {
        'weather_info': weather_info,
        'icon_path': weather_icons_path
    }
    return context

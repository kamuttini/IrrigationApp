from static.translation import WEATHER, WEEK
import requests
import datetime as DT
from .models import Area, Garden
from django.db.models import Q
from mysettings import WEATHER_API_KEY
from crontab import CronTab


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


# function to that return the frequency value for crontab jobs
def start_frequency(drange, hour):
    today = DT.date.today().day
    print(today)
    if drange == 1:
        result = '0 ' + str(hour) + ' * * *'
        return result
    elif drange == 2:
        if today % 2 == 0:
            result = '0 ' + str(hour) + ' 2-30/2 * *'
            return result
        else:
            result = '0 ' + hour + ' 1-30/2 * *'
            return result
    else:
        result = '0 ' + str(hour) + ' ' + str(today) + '-31/' + str(drange) + ' * *'
        return result


def stop_frequency(drange, hour, min):
    today = DT.date.today().day
    print(today)
    if min == '60':
        hour += 1
        min = '0'

    if drange == 1:
        result = min + str(hour) + ' * * *'
        return result
    elif drange == 2:
        if today % 2 == 0:
            result = min + str(hour) + ' 2-30/2 * *'
            return result
        else:
            result = min + hour + ' 1-30/2 * *'
            return result
    else:
        result = min + str(hour) + ' ' + str(today) + '-31/' + drange + ' * *'
        return result


# create command with esp32 ip address
def create_command(type, ip, garden, relay):
    fin = open("../static/commands/base_command.py", "rt")

    # read file contents to string
    data = fin.read()
    # replace all occurrences of the required string
    data = data.replace('ip_address', ip)
    data = data.replace('type', type)
    data = data.replace('relay', relay)
    # close the input file
    fin.close()
    # open the input file in write mode

    file_name = garden + '_relay' + relay + '_' + type + '.py'

    fin = open(file_name, "w")
    # overrite the input file with the resulting data
    fin.write(data)
    # close the file
    fin.close()


def schedule_irrigation(task):
    cron = CronTab(user='root')
    file_name_on = 'python ../static/commands/' + str(task.area.garden.id) + '_relay' + str(task.area.relay) + '_1.py'
    file_name_off = 'python ../static/commands/' + str(task.area.garden.id) + '_relay' + str(task.area.relay) + '_0.py'
    try:
        job1 = cron.find_command(command=file_name_on)
        job2 = cron.find_command(command=file_name_off)
    except:
        job1 = cron.new(command=file_name_on)
        job2 = cron.new(command=file_name_off)
    job1.setall(start_frequency(task.frequency, task.hour))
    job2.setall(start_frequency(task.frequency, task.hour.time.hour, task.duration))
    cron.write()


def remove_scheduled_irrigation(area):
    cron = CronTab(user='root')
    file_name_on = 'python ../static/commands/' + str(area.garden.id) + '_relay' + str(area.relay) + '_1.py'
    file_name_off = 'python ../static/commands/' + str(area.garden.id) + '_relay' + str(area.relay) + '_0.py'
    job1 = cron.find_command(command=file_name_on)
    job2 = cron.find_command(command=file_name_off)
    cron.remove(job1)
    cron.remove(job2)

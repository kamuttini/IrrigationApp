from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import GardenForm, AreaForm, EventForm
from .models import Area, Garden, Location
import requests


# Create your views here.
def index(request):
    garden_list = Garden.objects.order_by('name')
    context = {'garden_list': garden_list}
    return render(request, 'dashboard/index.html', context)


def detail(request, garden_id):
    garden_list = Garden.objects.order_by('name')
    garden = get_object_or_404(Garden, pk=garden_id)
    context = {
        'garden_list': garden_list,
        'garden': garden
    }

    return render(request, 'dashboard/detail.html', context)


def area_detail(request, area_id):
    garden = get_object_or_404(Garden)
    area = get_object_or_404(Area, pk=area_id)
    context = {
        'area': area,
        'garden': garden
    }
    return render(request, 'dashboard/area_detail.html', context)


def garden_create(request):
    form = GardenForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

    context = {
        'form': form
    }
    return render(request, 'dashboard/garden_create.html', context)


def area_create(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'dashboard/area_create.html', context)


def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'dashboard/event_create.html', context)


def garden_delete(request, garden_id):
    obj = get_object_or_404(Garden, pk=garden_id)
    # POST request
    if request.method == "POST":
        # confirming delete
        obj.delete()
        return HttpResponseRedirect('/')
    context = {
        'object': obj
    }
    return render(request, "dashboard/garden_delete.html", context)


def area_delete(request, area_id):
    obj = get_object_or_404(Area, pk=area_id)
    # POST request
    if request.method == "POST":
        # confirming delete
        obj.delete()
        return HttpResponseRedirect('/')
    context = {
        'object': obj
    }
    return render(request, "dashboard/area_delete.html", context)


def weather(request):
    location_list = Location.objects.order_by('city')
    location = get_object_or_404(Location)

    url = "https://api.climacell.co/v3/weather/forecast/daily"

    querystring = {"lat": location.lat, "lon": location.lon, "unit_system": "si", "start_time": "now",
                   "fields": "precipitation_probability,temp,weather_code",
                   "apikey": "6KIHRzYEnmDjo2nD68e6GWlHYGfbRIO2"}

    response = requests.request("GET", url, params=querystring).json()

    weather_info = {
        'temperature_min': str(response[0]['temp'][0]['min']['value']) + response[0]['temp'][0]['min']['units'],
        'temperature_max': str(response[0]['temp'][1]['max']['value']) + response[0]['temp'][1]['max']['units'],
        'precipitation': str(response[0]['precipitation_probability']['value']) +
                         response[0]['precipitation_probability']['units'],
        'description': response[0]['weather_code']['value']
    }

    context = {
        'location_list': location_list,
        'location': location,
        'weather_info': weather_info
    }

    return render(request, "dashboard/weather.html", context)

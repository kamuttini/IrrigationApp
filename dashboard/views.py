from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import GardenForm, AreaForm
from .models import Area, Garden, Irrigation
from notification.models import Notification
from .methods import *


# Create your views here.
@login_required(login_url="/authentication/login/")
def index(request):
    n = Notification.objects.filter(user=request.user, viewed=False).order_by('timestamp')
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    context = {'garden_list': garden_list,
               'notifications': n}

    for item in garden_list:
        item.next_rain = get_next_rain(item.city)

    return render(request, 'dashboard/index.html', context)


@login_required(login_url="/authentication/login/")
def detail(request, garden_id):
    from .methods import get_weather_info
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    garden = get_object_or_404(Garden, pk=garden_id)
    context = {
        'garden_list': garden_list,
        'garden': garden,
        'weather': get_weather_info(garden.city, "hourly")
    }

    return render(request, 'dashboard/detail.html', context)


@login_required(login_url="/authentication/login/")
def area_detail(request, area_id):
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    area = get_object_or_404(Area, pk=area_id)
    context = {
        'area': area,
        'garden_list': garden_list,

    }
    return render(request, 'dashboard/area_detail.html', context)


@login_required(login_url="/authentication/login/")
def irrigation(request, area_id, type):
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    area = get_object_or_404(Area, pk=area_id)
    irrigation_list = Irrigation.objects.filter(area=area)

    context = {
        'area': area,
        'garden_list': garden_list,
        'irrigation_list': irrigation_list
    }

    if type == "M":
        return render(request, 'dashboard/manual_irrigation.html', context)

    elif type == "C":
        return render(request, 'dashboard/calendar_irrigation.html', context)


@login_required(login_url="/authentication/login/")
def create(request, garden_id=None):
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    if garden_id:
        form = AreaForm(request.POST or None)
    else:
        form = GardenForm(request.POST or None)
    if form.is_valid():
        if garden_id:
            form.instance.garden = get_object_or_404(Garden, pk=garden_id)
        else:
            form.instance.user = request.user
        form.save()

        return HttpResponseRedirect('/')
    context = {
        'form': form,
        'garden_list': garden_list,
    }
    return render(request, 'dashboard/create.html', context)


@login_required(login_url="/authentication/login/")
def delete(request, id, type):
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    if type == "area":
        obj = get_object_or_404(Area, pk=id)
    else:
        obj = get_object_or_404(Garden, pk=id)

    # POST request
    if request.method == "POST":
        # confirming delete
        obj.delete()
        return HttpResponseRedirect('/')
    context = {
        'object': obj,
        'garden_list': garden_list,
    }
    return render(request, "dashboard/delete.html", context)


@login_required(login_url="/authentication/login/")
def weather(request):
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    weather_list = []
    locations = []

    for garden in garden_list:
        if garden.city not in locations:
            locations.append(garden.city)
    for city in locations:
        weather_list.append([city.city, get_weather_info(city, "daily")])

    context = {
        'garden_list': garden_list,
        'weather_list': weather_list,
    }
    return render(request, "dashboard/weather.html", context)


@login_required(login_url="authentication/login/")
def update(request, id, type):
    garden_list = Garden.objects.filter(user=request.user).order_by('name')
    if type == "area":
        obj = get_object_or_404(Area, id=id)
        form = AreaForm(request.POST or None, instance=obj)
    else:
        obj = get_object_or_404(Garden, id=id)
        form = GardenForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")

    context = {
        "form": form,
        'garden_list': garden_list,
    }

    return render(request, "dashboard/update.html", context)

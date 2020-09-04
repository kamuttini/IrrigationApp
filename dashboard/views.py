from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import GardenForm, AreaForm, EventForm
from .models import Area, Garden
from notification.models import Notification

# Create your views here.
@login_required(login_url="/authentication/login/")
def index(request):
    n = Notification.objects.filter(user=request.user, viewed=False).order_by('timestamp')
    garden_list = Garden.objects.order_by('name')
    context = {'garden_list': garden_list,
               'notifications': n}
    return render(request, 'dashboard/index.html', context)

@login_required(login_url="/authentication/login/")
def detail(request, garden_id):
    garden_list = Garden.objects.order_by('name')
    garden = get_object_or_404(Garden, pk=garden_id)
    context = {
        'garden_list': garden_list,
        'garden': garden
    }

    return render(request, 'dashboard/detail.html', context)

@login_required(login_url="/authentication/login/")
def area_detail(request, area_id):
    garden_list = Garden.objects.order_by('name')
    area = get_object_or_404(Area, pk=area_id)
    context = {
        'area': area,
        'garden_list': garden_list,

    }
    return render(request, 'dashboard/area_detail.html', context)

@login_required(login_url="/authentication/login/")
def garden_create(request):
    garden_list = Garden.objects.order_by('name')
    form = GardenForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

    context = {
        'form': form,
        'garden_list': garden_list,
    }
    return render(request, 'dashboard/create.html', context)

@login_required(login_url="/authentication/login/")
def area_create(request):
    garden_list = Garden.objects.order_by('name')
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/')
    context = {
        'form': form,
        'garden_list': garden_list,
    }
    return render(request, 'dashboard/create.html', context)

@login_required(login_url="/authentication/login/")
def event_create(request):
    garden_list = Garden.objects.order_by('name')
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/')
    context = {
        'form': form,
        'garden_list': garden_list,
    }
    return render(request, 'dashboard/create.html', context)

@login_required(login_url="/authentication/login/")
def garden_delete(request, garden_id):
    garden_list = Garden.objects.order_by('name')
    obj = get_object_or_404(Garden, pk=garden_id)
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
def area_delete(request, area_id):
    garden_list = Garden.objects.order_by('name')
    obj = get_object_or_404(Area, pk=area_id)
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
    from .methods import get_weather_info
    garden_list = Garden.objects.order_by('name')

    locations = []

    for garden in garden_list:
        weather_list = []
        if garden.city not in locations:
            locations.append(garden.city)
    for city in locations:
        five_days_weather = []
        for j in range(5):
            five_days_weather.append(get_weather_info(city, j))
        weather_list.append([city.city, five_days_weather])

    print(weather_list)

    context = {
        'garden_list': garden_list,
        'weather_list': weather_list,
    }
    return render(request, "dashboard/weather.html", context)

@login_required(login_url="authentication/login/")
def garden_update(request, garden_id):
    garden_list = Garden.objects.order_by('name')
    obj = get_object_or_404(Garden, id=garden_id)

    form = GardenForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")

    context = {
        "form": form,
        'garden_list': garden_list,
    }

    return render(request, "dashboard/update.html", context)

from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
from notification.models import Notification
from .methods import *


# information requested in all views
def custom_processor(request):
    if request.user.is_authenticated:
        garden_list = Garden.objects.filter(user=request.user).order_by('name')
        n = Notification.objects.filter(user=request.user, viewed=False).order_by('timestamp')

        if request.GET and 'q' in request.GET:
            query = request.GET.get('q')
            area_search, garden_search = search(request)
            return {'query': query, 'area_search': area_search, 'garden_search': garden_search,
                    'garden_list': garden_list, 'notifications': n}

        return {'garden_list': garden_list, 'notifications': n}

    return {}


# views here.
@login_required(login_url="/authentication/login/")  # access permitted only if user is logged in
def index(request):
    garden_list = Garden.objects.filter(user=request.user).order_by('name')

    # for each garden get request to update next_rain field.
    for item in garden_list:
        item.next_rain = get_rain(item.city, 'next')

    # form to create new garden
    form = GardenForm(request.POST or None)
    if form.is_valid():
        form.instance.user = request.user  # set current user as user
        form.save()
        return HttpResponseRedirect('/')

    context = {'garden_list': garden_list,
               'form': form
               }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url="/authentication/login/")
def detail(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)

    # form to create new area
    create_form = AreaForm(request.POST or None)
    if request.method == "POST" and 'create' in request.POST:
        if create_form.is_valid():
            create_form.instance.garden = get_object_or_404(Garden, pk=garden_id)
            create_form.save()

            # schedule future irrigation for this area
            calendar_irrigation = ScheduledIrrigation(area=create_form.instance)
            calendar_irrigation.save()

    # delete garden
    if request.method == "POST" and 'delete' in request.POST:
        garden.delete()
        return HttpResponseRedirect('/')

    # update garden info
    update_form = GardenForm(request.POST or None, instance=garden, initial={'city': garden.city})
    if request.method == "POST" and 'update' in request.POST:
        if update_form.is_valid():
            update_form.save()

    context = {
        'garden': garden,
        'weather': get_weather_info(garden.city, "hourly"),
        'create_form': create_form,
        'update_form': update_form
    }

    return render(request, 'dashboard/detail.html', context)


@login_required(login_url="/authentication/login/")
def area_detail(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    irrigation_list = Irrigation.objects.filter(area=area).order_by('-start')[:20]

    if request.method == "POST" and 'delete' in request.POST:
        area.delete()
        return HttpResponseRedirect('/')

    update_form = AreaForm(request.POST or None, instance=area)
    if request.method == "POST" and 'update' in request.POST:
        if update_form.is_valid():
            update_form.save()

    context = {
        'area': area,
        'update_form': update_form,
        'irrigation_list': irrigation_list,
    }

    return render(request, 'dashboard/area_detail.html', context)


@login_required(login_url="/authentication/login/")
def irrigation(request, area_id, type):
    area = get_object_or_404(Area, pk=area_id)
    irrigation_list = Irrigation.objects.filter(area=area).order_by('-start')
    context = {
        'area': area,
        'irrigation_list': irrigation_list,
    }

    # different process for each type of irrigation Manual (M) , Scheduled (C), Smart (S)
    if type == "M":
        irrigation = Irrigation.objects.filter(area=area, end__gte=timezone.now()).order_by('-start')[:1]
        context['irrigation'] = irrigation

        if request.method == 'POST' and 'create' in request.POST:
            Irrigation.objects.create(area=area, end=timezone.now() + datetime.timedelta(
                minutes=int(request.POST.get('value', ""))))

        if irrigation:
            if request.method == 'POST' and 'delete' in request.POST:
                irrigation[0].end = timezone.now()  # if the irrigation is stop before prefixed time, current time value is passed as end
                irrigation[0].save()
                return render(request, 'dashboard/manual_irrigation.html', context)

        return render(request, 'dashboard/manual_irrigation.html', context)

    elif type == "C":
        irrigation_settings = get_object_or_404(ScheduledIrrigation, area=area)
        form = CalendarIrrigationForm(request.POST or None, instance=irrigation_settings)

        if form.is_valid():
            form.save()

        context['form'] = form
        context['irrigation_settings'] = irrigation_settings
        return render(request, 'dashboard/scheduled_irrigation.html', context)

    elif type == "S":
        return render(request, 'dashboard/smart_irrigation.html', context)


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


@login_required(login_url="/authentication/login/")
def settings(request):
    settings = get_object_or_404(Setting, user=request.user)
    user_form = PasswordChangeForm(request.user, request.POST or None)
    update_form = SettingsForm(request.POST or None, instance=settings)

    if request.method == "POST":
        if update_form.is_valid() and 'update_email' in request.POST:
            update_form.save()
            return HttpResponseRedirect('/')

        if user_form.is_valid() and 'update_password' in request.POST:
            user_form.save()
            return HttpResponseRedirect('/')

    context = {
        'update_form': update_form,
        'user_form': user_form
    }
    return render(request, "dashboard/settings.html", context)


def update_temperature(request, garden_id, temp):
    try:
        garden = get_object_or_404(Garden, id=garden_id)
        garden.temperature = temp
        garden.save()
    except:
        return HttpResponseNotFound(
            "<h1>Operazione non completata</h1><br><p>L'indirizzo potrebbe essere errato o l'id inesistente</p>")

    return HttpResponse(status=200)


def update_humidity(request, area_id, humidity):
    try:
        area = get_object_or_404(Area, id=area_id)
        area.humidity = humidity
        area.save()
    except:
        return HttpResponseNotFound(
            "<h1>Operazione non completata</h1><br><p>L'indirizzo potrebbe essere errato o l'id inesistente</p>")
    return HttpResponse(status=200)


def register_rain(request, garden_id):
    try:
        garden = get_object_or_404(Garden, id=garden_id)
        Rain.objects.create(garden=garden)
    except:
        return HttpResponseNotFound(
            "<h1>Operazione non completata</h1><br><p>L'indirizzo potrebbe essere errato o l'id inesistente</p>")
    return HttpResponse(status=201)


def register_rain_halt(request, garden_id):
    try:
        rain = Rain.objects.filter(garden=garden_id).latest('start')
        rain.end = timezone.now()
        rain.save()
    except:
        return HttpResponseNotFound(
            "<h1>Operazione non completata</h1><br><p>L'indirizzo potrebbe essere errato o l'id inesistente</p>")
    return HttpResponse(status=200)

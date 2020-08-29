from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import GardenForm, AreaForm, EventForm
from .models import Area
from .models import Garden


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

    return render(request, 'dashboard/detail.html',  context)


def area_detail(request, area_id):
    garden = get_object_or_404(Garden)
    area = get_object_or_404(Area, pk=area_id)
    return render(request, 'dashboard/area_detail.html', {'area': area, 'garden' : garden})


def garden_create(request):
    form = GardenForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

    context = {
        'form': form
    }
    return render(request, 'dashboard/create.html', context)


def area_create(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'dashboard/create.html', context)


def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'dashboard/create.html', context)


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
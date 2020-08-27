from django.http import HttpResponse
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
    garden = get_object_or_404(Garden, pk=garden_id)
    return render(request, 'dashboard/detail.html', {'garden': garden} )

def garden_create(request):
    form = GardenForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'dashboard/garden_create.html', context)

def area_create(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'dashboard/area_create.html', context)

def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'dashboard/event_create.html', context)
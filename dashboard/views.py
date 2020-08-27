from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

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
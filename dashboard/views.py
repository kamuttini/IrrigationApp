from django.http import HttpResponse
from django.shortcuts import render

from .models import Area
from .models import Garden

# Create your views here.
def index(request):
    garden_list = Garden.objects.order_by('name')[:5]
    context = {'garden_list': garden_list}
    return render(request, 'dashboard/index.html', context)

def detail(request, area_id):
    return HttpResponse("You're looking at area %s." % area_id)
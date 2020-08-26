from django.http import HttpResponse
from django.shortcuts import render

from .models import Area

# Create your views here.
def index(request):
    latest_irrigation_list = Area.objects.order_by('last_irrigation')[:5]
    context = {'latest_irrigation_list': latest_irrigation_list}
    return render(request, 'dashboard/index.html', context)

def detail(request, area_id):
    return HttpResponse("You're looking at area %s." % area_id)
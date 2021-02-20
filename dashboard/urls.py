from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:garden_id>/', views.detail, name='detail'),
    path('<int:area_id>/irrigation/<slug:type>', views.irrigation, name='irrigation'),
    path('<int:area_id>/area_detail/', views.area_detail, name='area_detail'),
    path('weather/', views.weather, name='weather'),
    path('settings/', views.settings, name='settings'),
    path('update_temperature/<int:garden_id>/<temp>/', views.update_temperature, name='update_temperature'),
    path('update_humidity/<int:area_id>/<int:humidity>/', views.update_humidity, name='update_humidity'),
    path('register_rain/<int:garden_id>/', views.register_rain, name='register_rain'),
    path('register_rain_halt/<int:garden_id>/', views.register_rain_halt, name='register_rain_halt'),
    path('register_irrigation/<slug:t>/<int:area_id>/<int:duration>/', csrf_exempt(views.register_irrigation), name='register_irrigation')

]
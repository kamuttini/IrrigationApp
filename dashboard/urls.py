from django.urls import path

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
]
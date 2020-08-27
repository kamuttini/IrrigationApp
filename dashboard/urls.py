from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:garden_id>/', views.detail, name='detail'),
    path('garden_create/', views.garden_create, name='garden_create'),
    path('area_create/', views.area_create, name='area_create'),
    path('event_create/', views.event_create, name='event_create')

]
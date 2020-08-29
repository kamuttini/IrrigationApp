from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:garden_id>/', views.detail, name='detail'),
    path('garden_create/', views.garden_create, name='garden_create'),
    path('area_create/', views.area_create, name='area_create'),
    path('event_create/', views.event_create, name='event_create'),
    path('<int:garden_id>/garden_delete/', views.garden_delete, name='garden_delete'),
    path('<int:area_id>/area_delete/', views.area_delete, name='area_delete'),
    path('<int:area_id>/area_detail/', views.area_detail, name='area_detail')


]
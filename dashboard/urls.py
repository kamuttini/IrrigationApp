from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:garden_id>/', views.detail, name='detail'),
    path('<int:id>/update/<slug:type>', views.update, name='update'),
    path('<int:area_id>/manual_irrigation/', views.manual_irrigation, name='manual_irrigation'),
    path('garden_create/', views.create, name='garden_create'),
    path('<int:garden_id>/area_create/', views.create, name='area_create'),
    path('<int:id>/delete/<slug:type>', views.delete, name='delete'),
    path('<int:area_id>/area_detail/', views.area_detail, name='area_detail'),
    path('weather/', views.weather, name='weather')
]
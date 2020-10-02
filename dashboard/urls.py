from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:garden_id>/', views.detail, name='detail'),
    path('<int:area_id>/irrigation/<slug:type>', views.irrigation, name='irrigation'),
    path('<int:area_id>/area_detail/', views.area_detail, name='area_detail'),
    path('weather/', views.weather, name='weather')
]
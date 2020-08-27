from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:garden_id>/', views.detail, name='detail'),
    path('garden_create/', views.garden_create, name='garden_create'),
]
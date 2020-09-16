from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'agenda'
urlpatterns = [
    url(r'^$', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<event_id>/', views.event, name='event_edit'),
    path('event/delete/<event_id>/', views.event_delete, name='event_delete')
]

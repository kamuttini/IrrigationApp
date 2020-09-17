from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'agenda'
urlpatterns = [
    url(r'^$', views.CalendarView.as_view(), name='calendar'),
    path('new/', views.event, name='event_new'),
    path('<event_id>/edit/', views.event, name='event_edit'),
    path('<event_id>/delete/', views.event_delete, name='event_delete')
]

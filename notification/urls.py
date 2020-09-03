from django.urls import path
from . import views
urlpatterns = [
  path('show/<int:notification_id>/', views.show_notification),
  path('delete/', views.delete_notification)
]
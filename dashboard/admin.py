from django.contrib import admin

# Register your models here.

from .models import Garden, Area

admin.site.register(Garden)
admin.site.register(Area)


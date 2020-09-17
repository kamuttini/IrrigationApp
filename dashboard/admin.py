from django.contrib import admin

# Register your models here.

from .models import Garden, Area, Location, Irrigation

admin.site.register(Garden)
admin.site.register(Area)
admin.site.register(Location)
admin.site.register(Irrigation)


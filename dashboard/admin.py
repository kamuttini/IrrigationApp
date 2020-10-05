from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Garden)
admin.site.register(Area)
admin.site.register(Location)
admin.site.register(Irrigation)
admin.site.register(CalendarIrrigation)
admin.site.register(Setting)

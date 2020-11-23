from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

from .models import *

admin.site.register(Garden)
admin.site.register(Area)
admin.site.register(Location)
admin.site.register(Irrigation)
admin.site.register(ScheduledIrrigation)
admin.site.register(Setting)


class SettingInline(admin.StackedInline):
    model = Setting
    can_delete = False
    verbose_name_plural = 'setting'


class UserAdmin(BaseUserAdmin):
    inlines = (SettingInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
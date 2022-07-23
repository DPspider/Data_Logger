from django.contrib import admin

from dashboard.models import ProgrammableParameters, Report, UserProfile, Devices

# Register your models here.

admin.site.register(Report)
admin.site.register(Devices)
admin.site.register(UserProfile)
admin.site.register(ProgrammableParameters)

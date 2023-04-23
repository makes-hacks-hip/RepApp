"""
Admin interface configuration for RepApp.
"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Organisator, Cafe, Question, Device,
                     Reparateur, Appointment, Guest, Candidate)


class DeviceAdmin(ImportExportModelAdmin):
    resource_classes = [Device]


admin.site.register(Organisator)
admin.site.register(Cafe)
admin.site.register(Question)
admin.site.register(Guest)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Reparateur)
admin.site.register(Appointment)
admin.site.register(Candidate)

"""
Admin interface configuration for RepApp.
"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import resources
from .models import (Organisator, Cafe, Question, Device,
                     Reparateur, Appointment, Guest, Candidate)


class GuestResource(resources.ModelResource):
    class Meta:
        model = Guest

    @staticmethod
    def get_display_name():
        return "Gäste"


class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device

    @staticmethod
    def get_display_name():
        return "Geräte"


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

    @staticmethod
    def get_display_name():
        return "Fragen"


class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointment

    @staticmethod
    def get_display_name():
        return "Termine"


class CandidateResource(resources.ModelResource):
    class Meta:
        model = Candidate

    @staticmethod
    def get_display_name():
        return "Kandidaten"


class ExportAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_classes = [
        DeviceResource,
        GuestResource,
        QuestionResource,
        AppointmentResource,
        CandidateResource,
    ]


admin.site.register(Organisator)
admin.site.register(Cafe)
admin.site.register(Question, ExportAdmin)
admin.site.register(Guest, ExportAdmin)
admin.site.register(Device, ExportAdmin)
admin.site.register(Reparateur)
admin.site.register(Appointment, ExportAdmin)
admin.site.register(Candidate, ExportAdmin)

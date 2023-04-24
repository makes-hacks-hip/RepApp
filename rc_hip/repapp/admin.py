"""
Admin interface configuration for RepApp.
"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import resources
from .models import (Organisator, Cafe, Question, Device, CustomUser,
                     Reparateur, Appointment, Guest, Candidate, OneTimeLogin)


class GuestResource(resources.ModelResource):
    """
    Resource wrapper for Guest model.
    """
    class Meta:
        """
        Meta data for resource model.
        """
        model = Guest

    @staticmethod
    def get_display_name():
        return "Gäste"


class DeviceResource(resources.ModelResource):
    """
    Resource wrapper for Device model.
    """
    class Meta:
        """
        Meta data for resource model.
        """
        model = Device

    @staticmethod
    def get_display_name():
        return "Geräte"


class QuestionResource(resources.ModelResource):
    """
    Resource wrapper for Question model.
    """
    class Meta:
        """
        Meta data for resource model.
        """
        model = Question

    @staticmethod
    def get_display_name():
        return "Fragen"


class AppointmentResource(resources.ModelResource):
    """
    Resource wrapper for Appointment model.
    """
    class Meta:
        """
        Meta data for resource model.
        """
        model = Appointment

    @staticmethod
    def get_display_name():
        return "Termine"


class CandidateResource(resources.ModelResource):
    """
    Resource wrapper for Candidate model.
    """
    class Meta:
        """
        Meta data for resource model.
        """
        model = Candidate

    @staticmethod
    def get_display_name():
        return "Kandidaten"


class ExportAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
    Admin model for data export, supporting buttons and action.
    """
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
admin.site.register(CustomUser)
admin.site.register(OneTimeLogin)

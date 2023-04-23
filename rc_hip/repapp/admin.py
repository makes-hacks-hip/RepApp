"""
Admin interface configuration for RepApp.
"""
from django.contrib import admin
from .models import (Organisator, Cafe, Question, Device,
                     Reparateur, Appointment, Guest, Candidate)

admin.site.register(Organisator)
admin.site.register(Cafe)
admin.site.register(Question)
admin.site.register(Guest)
admin.site.register(Device)
admin.site.register(Reparateur)
admin.site.register(Appointment)
admin.site.register(Candidate)

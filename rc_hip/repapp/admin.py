from django.contrib import admin

from .models import Organisator, Cafe, Question, Device, Reparateur, Appointment

admin.site.register(Organisator)
admin.site.register(Cafe)
admin.site.register(Question)
admin.site.register(Device)
admin.site.register(Reparateur)
admin.site.register(Appointment)

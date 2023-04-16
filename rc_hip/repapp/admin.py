from django.contrib import admin

from .models import Organisator, Cafe, Frage, Gerät, Reparateur, Termin

admin.site.register(Organisator)
admin.site.register(Cafe)
admin.site.register(Frage)
admin.site.register(Gerät)
admin.site.register(Reparateur)
admin.site.register(Termin)

from django.contrib import admin
from .models import OneTimeLogin


@admin.register(OneTimeLogin)
class OneTimeLoginAdmin(admin.ModelAdmin):
    list_display = ['user', 'url', 'login_used', 'login_date', 'created']
    list_filter = ['user', 'url', 'login_used', 'login_date', 'created']
    search_fields = ['user', 'url']
    raw_id_fields = ['user']
    date_hierarchy = 'created'
    ordering = ['created', 'user', 'url']

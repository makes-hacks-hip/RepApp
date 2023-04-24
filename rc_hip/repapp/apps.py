"""
RepApp application.
"""
from django.apps import AppConfig


class RepappConfig(AppConfig):
    """
    Django config for RepApp application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repapp'

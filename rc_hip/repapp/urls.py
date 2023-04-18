"""
Urls of RepApp.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:cafe_id>/", views.register_device, name="register_device"),
]

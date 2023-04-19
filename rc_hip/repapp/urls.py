"""
Urls of RepApp.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "cafe/<int:cafe_id>/",
        views.RegisterDeviceFormView.as_view(),
        name="register_device"
    ),
    path(
        "cafe/<int:cafe_id>/device/<str:device_identifier>/<str:mail>",
        views.RegisterGuestFormView.as_view(),
        name="register_guest"
    ),
    path("cafe/<int:cafe_id>/device/<str:device_identifier>/guest/<str:guest_identifier>",
         views.register_device_final, name="register_device_final"),
]

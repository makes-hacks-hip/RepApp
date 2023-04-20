"""
Urls of RepApp.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "cafe/<int:cafe>/",
        views.RegisterDeviceFormView.as_view(),
        name="register_device"
    ),
    path(
        "cafe/<int:cafe>/device/<str:deviceentifier>/<str:mail>",
        views.RegisterGuestFormView.as_view(),
        name="register_guest"
    ),
    path("cafe/<int:cafe>/device/<str:deviceentifier>/guest/<str:guestentifier>",
         views.register_device_final, name="register_device_final"),
    path("confirm/<str:deviceentifier>/code/<str:device_secret>",
         views.register_device_confirm, name="register_device_final"),
    path("device/<str:deviceentifier>",
         views.device_view, name="view_device"),
]

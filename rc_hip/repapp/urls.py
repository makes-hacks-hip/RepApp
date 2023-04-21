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
        "cafe/<int:cafe>/device/<str:device_identifier>/mail/<str:mail>/",
        views.RegisterGuestFormView.as_view(),
        name="register_guest"
    ),
    path("cafe/<int:cafe>/device/<str:device_identifier>/confirm/",
         views.register_device_final, name="register_device_final"),
    path("device/<str:device_identifier>/",
         views.device_view, name="view_device"),
]

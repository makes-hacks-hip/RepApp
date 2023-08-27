"""
Urls of RepApp.
"""
from django.urls import path
from . import views


app_name = 'one_time_login'


urlpatterns = [
    path("<str:secret>/", views.one_time_login, name="login"),
]

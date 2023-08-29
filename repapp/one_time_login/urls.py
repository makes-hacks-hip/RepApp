"""
Urls of RepApp.
"""
from django.urls import path
from . import views


app_name = 'one_time_login'


urlpatterns = [
    path("protected/", views.protected_test, name="protected"),
    path("dummy/", views.dummy_content, name="dummy"),
    path("<str:secret>/", views.login_view, name="login"),
]

"""
Urls of RepApp.
"""
import sys
import logging
from django.urls import path
from django.conf import settings
from . import views


app_name = 'one_time_login'


urlpatterns = [
    path("<str:secret>/", views.login_view, name="login"),
]

if settings.DEBUG or sys.argv[1:2] == ['test']:
    logging.info('one_time_login: enable protected test URL')
    urlpatterns += [
        path("protected/", views.protected_test, name="protected"),
    ]

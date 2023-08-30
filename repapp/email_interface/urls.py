"""
Urls of RepApp.
"""
import sys
import logging
from django.urls import path
from django.conf import settings
from . import views


app_name = 'email_interface'


urlpatterns = [
    path("process/", views.process, name="process"),
    path("sent/", views.my_sent_mails, name="my_sent_mails"),
    path("received/", views.my_received_mails, name="my_received_mails"),
    path("attachments/", views.my_attachments, name="my_attachments"),
    path("<int:id>/view", views.mail_thread, name="mail_thread"),
]

if settings.DEBUG or sys.argv[1:2] == ['test']:
    logging.info('email_interface: enable test and debug URLs')
    urlpatterns += [
        path("test-mail/", views.send_test_mail, name="send_test_mail"),
        path("send-mail/", views.SendMailView.as_view(), name="send_mail"),
    ]

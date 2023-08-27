import os
import datetime
import random
import logging
from hashlib import sha256
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from .models import OneTimeLogin


logger = logging.getLogger(__name__)


def create_one_time_login(user, url) -> str:
    """
    create_one_time_login creates a one time login object for guest user logins.
    """
    secret = sha256(
        f'{user.email}{url}{datetime.datetime.now()}{random.randint(0,9999999)}'.encode(
            'utf-8')
    ).hexdigest()
    secret_hash = sha256(secret.encode('utf-8')).hexdigest()
    otl = OneTimeLogin(
        secret=secret_hash,
        user=user,
        url=url,
    )
    otl.save()
    return secret


def send_one_time_login_mail(secret, mail, request):
    """
    Send a mail with a one time login link.
    """
    url = request.build_absolute_uri(
        f'/onetimelogin/{secret}/')
    subject = render_to_string('one_time_login/mail_subject.txt', {
        'organization': settings.ORGANIZATION,
    }).replace('\n', '')
    html = render_to_string('one_time_login/mail_content.html', {
        'link': url,
        'organization': settings.ORGANIZATION,
    })
    text = render_to_string('one_time_login/mail_content.html', {
        'link': url,
        'organization': settings.ORGANIZATION,
    })

    send_ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[mail],
        fail_silently=True,
        html_message=html
    )

    if send_ok > 0:
        messages.add_message(request, messages.INFO, _(
            'A new login link was sent by mail.'))

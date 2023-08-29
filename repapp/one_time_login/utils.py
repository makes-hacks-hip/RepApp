import datetime
import random
import logging
from hashlib import sha256
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.contrib.auth import authenticate
from .models import OneTimeLogin


logger = logging.getLogger(__name__)


def create_one_time_login(user, url) -> OneTimeLogin:
    """
    create_one_time_login creates a one time login object for guest user logins.
    """
    secret = sha256(
        f'{user.email}{url}{datetime.datetime.now()}{random.randint(0,9999999)}'.encode(
            'utf-8')
    ).hexdigest()

    otl = OneTimeLogin(
        secret=secret,
        user=user,
        url=url,
    )
    otl.save()

    logger.debug('One time login created for user %s and URL %s', user, url)

    return otl


def send_one_time_login_mail(secret, mail, request, language=None):
    """
    Send a mail with a one time login link.
    """
    if language is None:
        language = settings.LANGUAGE_CODE

    url = request.build_absolute_uri(reverse_lazy(
        'one_time_login:login', kwargs={'secret': secret}))

    cur_language = translation.get_language()
    try:
        translation.activate(language)
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
    finally:
        translation.activate(cur_language)

    send_ok = send_mail(
        subject=subject,
        message=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[mail],
        fail_silently=True,
        html_message=html
    )

    logger.debug('One time login mail sent to mail %s', mail)

    if send_ok > 0:
        messages.add_message(request, messages.INFO, _(
            'A new login link was sent by mail.'))
    else:
        messages.add_message(request, messages.ERROR, _(
            'Sending of one time login link failed!'))


def one_time_login(request, secret):
    """
    Evaluates a one time login request.
    """
    try:
        otl = OneTimeLogin.objects.get(secret=secret)
    except OneTimeLogin.DoesNotExist:
        logger.info('No one time login for secret %s', secret)
        return (None, None)

    if otl.login_used:
        messages.add_message(request, messages.ERROR,
                             _('Login was used already.'))
        logger.info('One time login with secret %s for user %s and URL %s was already used',
                    secret, otl.user, otl.url)

        if otl.user.email:
            logger.debug(
                'Creating and sending one time login for user %s and URL %s', otl.user, otl.url)
            # create and send a new one time login
            new_secret = create_one_time_login(otl.user, otl.url)
            send_one_time_login_mail(new_secret, otl.user.email, request)

        return (None, None)

    else:
        otl.login_used = True
        otl.login_date = now()
        otl.save()

    user = authenticate(request, username=secret, password=None)

    logger.info('Authenticated user %s with one time login.', user)

    return (user, otl.url)

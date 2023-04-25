import os
import unicodedata
import datetime
import random
from hashlib import sha256
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from repapp.models import Organisator, Reparateur, OneTimeLogin


def create_one_time_login(user, url) -> str:
    """
    create_one_time_login create a one time login object for user logins.
    """
    secret = sha256(
        f'{user.email}{url}{datetime.datetime.now()}{random.randint(0,9999999)}'.encode(
            'utf-8')
    ).hexdigest()
    hash = sha256(secret.encode('utf-8')).hexdigest()
    otl = OneTimeLogin(
        secret=hash,
        user=user,
        url=url,
    )
    otl.save()
    return secret


def send_one_time_login_mail(secret, mail, request):
    url = request.build_absolute_uri(
        f'/onetimelogin/{secret}/')
    subject = render_to_string(
        'repapp/mail/mail_one_time_login_subject.html').replace('\n', '')
    text = render_to_string('repapp/mail/mail_one_time_login_text.html', {
        'link': url,
    })
    html = render_to_string('repapp/mail/mail_one_time_login_html.html', {
        'link': url,
    })

    ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[mail],
        fail_silently=True,
        html_message=html
    )

    if ok > 0:
        messages.add_message(request, messages.INFO,
                             'Sie haben einen neuen Login per eMail erhalten.')


def create_repapp_user(user):
    organisator = Organisator.objects.filter(mail=user.email).first()
    if not organisator:
        reparateur = Reparateur.objects.filter(mail=user.email).first()
        if not reparateur:
            reparateur = Reparateur(
                name=user.username,
                mail=user.email,
            )
            reparateur.save()
        else:
            reparateur.name = user.username
            reparateur.save()
    else:
        organisator.name = user.username
        organisator.save()


def generate_username(email):
    # Using Python 3 and Django 1.11+, usernames can contain alphanumeric
    # (ascii and unicode), _, @, +, . and - characters. So we normalize
    # it and slice at 150 characters.
    return unicodedata.normalize('NFKC', email)[:150]


def send_confirmation_mails(device, guest, cafe, request):
    organizers = []
    for organizer in Organisator.objects.all():
        organizers.append(organizer.mail)

    text = render_to_string('repapp/mail/notice_new_device.html', {
        'guest': device.guest,
        'device': device,
        'cafe': device.cafe,
    })

    send_mail(
        subject=f"Neues Gerät { device.device }",
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=organizers,
        fail_silently=True
    )

    path = reverse('view_device', kwargs={
                   'device_identifier': device.identifier})
    url = request.build_absolute_uri(path)
    secret = create_one_time_login(guest.user, url)
    login_url = request.build_absolute_uri(f'/onetimelogin/{secret}/')

    subject = render_to_string('repapp/mail/mail_register_device_subject.html', {
        'cafe': cafe,
    }).replace('\n', '')
    text = render_to_string('repapp/mail/mail_register_device_text.html', {
        'guest': guest,
        'device': device,
        'cafe': cafe,
        'login_url': login_url,
    })
    html = render_to_string('repapp/mail/mail_register_device_html.html', {
        'guest': guest,
        'device': device,
        'cafe': cafe,
        'login_url': login_url,
    })

    mail_count = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[f"{guest.mail}"],
        fail_silently=True,
        html_message=html
    )

    if mail_count > 0:
        device.confirmed = True
        device.save()
    else:
        messages.add_message(request, messages.ERROR,
                             'Fehler beim senden der Bestätigungs-eMail!')


def send_guest_account_mail(guest, password, request):
    url = request.build_absolute_uri('/guest/profile/')
    subject = render_to_string(
        'repapp/mail/mail_new_guest_subject.html').replace('\n', '')
    text = render_to_string('repapp/mail/mail_new_guest_text.html', {
        'link': url,
        'username': guest.user.email,
        'password': password,
    })
    html = render_to_string('repapp/mail/mail_new_guest_html.html', {
        'link': url,
        'username': guest.user.email,
        'password': password,
    })

    ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[f"{guest.user.email}"],
        fail_silently=True,
        html_message=html
    )

    if ok > 0:
        messages.add_message(request, messages.INFO,
                             'Sie haben ihre Benutzerdaten per eMail erhalten.')


def is_member(user):
    organisator = Organisator.objects.filter(mail=user.email).first()
    reparateur = Reparateur.objects.filter(mail=user.email).first()
    return organisator or reparateur


def device_directory_path(instance, filename):
    """
    device_directory_path generates a device-specific storage path for file uploads.
    """
    return f'device_{instance.identifier}/{filename}'

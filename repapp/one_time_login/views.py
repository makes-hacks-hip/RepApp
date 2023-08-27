import time
from hashlib import sha256
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from .models import OneTimeLogin
from .api import create_one_time_login, send_one_time_login_mail


def one_time_login(request, secret: str):
    """
    View for one time login.
    """
    # waste a little time as brute force protection
    time.sleep(1)

    secret_hash = sha256(secret.encode('utf-8')).hexdigest()
    otl = get_object_or_404(OneTimeLogin, secret=secret_hash)

    if otl.login_used:
        messages.add_message(request, messages.ERROR,
                             _('Login was used already.'))
        new_secret = create_one_time_login(otl.user, otl.url)
        send_one_time_login_mail(new_secret, otl.user.email, request)
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        otl.login_used = True
        otl.login_date = now()
        otl.save()

    user = authenticate(request, username=secret_hash, password=None)

    if user is not None:
        login(request, user)
        messages.add_message(request, messages.INFO, _('Login successful!'))
        return HttpResponseRedirect(otl.url)
    else:
        messages.add_message(request, messages.ERROR, _('Login failed!'))
        return HttpResponseRedirect(reverse_lazy('index'))

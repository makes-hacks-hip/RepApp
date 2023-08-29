import time
import logging
from hashlib import sha256
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from .models import OneTimeLogin
from .utils import one_time_login


logger = logging.getLogger(__name__)


def login_view(request, secret: str):
    """
    View for one time login.
    """
    # waste a little time as brute force protection
    time.sleep(1)

    logger.debug('one_time_login: secret %s', secret)

    (user, url) = one_time_login(request, secret)

    logger.debug('one_time_login: user %s, url %s', user, url)

    if user is not None:
        login(request, user)
        messages.add_message(request, messages.INFO, _('Login successful!'))
        if url is not None:
            logger.debug('one_time_login: redirecting to url %s', url)
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/')

    messages.add_message(request, messages.ERROR, _('Login failed!'))
    return HttpResponseRedirect('/')


@login_required
def protected_test(request):
    return HttpResponse('protected content')


@login_required
def dummy_content(request):
    return HttpResponse("dummy content")

"""
Authentication backends for RepApp.
"""
import logging
from django.contrib.auth.backends import ModelBackend
from .models import OneTimeLogin


logger = logging.getLogger(__name__)


class OneTimeLoginBackend(ModelBackend):
    """
    OneTimeLoginBackend implements a login using a onetime secret.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        login = OneTimeLogin.objects.filter(secret=username).first()
        if login:
            logger.debug(
                'One time login authentication for secret %s was successful', username)
            return login.user
        else:
            logger.info(
                'One time login authentication for secret %s failed!', username)
            return None

"""
Authentication backends for RepApp.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .utils import generate_username, create_repapp_user
from .models import OneTimeLogin


class OneTimeLoginBackend(ModelBackend):
    """
    OneTimeLoginBackend implements a login using a onetime secret.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f'authenticate {username}')
        login = OneTimeLogin.objects.filter(secret=username).first()
        if login:
            return login.user
        else:
            return None


class EmailBackend(ModelBackend):
    """
    EmailBackend allows a login using email address as username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class KeycloakOIDCAB(OIDCAuthenticationBackend):
    """
    KeycloakOIDCAB allows a login using Open ID Connect
    (with the Repair-Café Keycloak Single Sign On server)
    """

    def create_user(self, claims):
        user = super(KeycloakOIDCAB, self).create_user(claims)

        user.username = claims.get(
            'preferred_username', generate_username(user.email))
        user.save()

        create_repapp_user(user)

        return user

    def update_user(self, user, claims):
        user.username = claims.get(
            'preferred_username', generate_username(user.email))
        user.save()

        create_repapp_user(user)

        return user

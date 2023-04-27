"""
Authentication backends for RepApp.
"""
import unicodedata
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .models import OneTimeLogin, Organisator, Reparateur

logger = logging.getLogger(__name__)


def generate_username(email):
    """
    Generate a valid user name form the mail address.
    """
    # Using Python 3 and Django 1.11+, usernames can contain alphanumeric
    # (ascii and unicode), _, @, +, . and - characters. So we normalize
    # it and slice at 150 characters.
    return unicodedata.normalize('NFKC', email)[:150]


def create_repapp_user(user):
    """
    Create the RepApp user objects for the new user.
    If a user logs in using OIDC it is a member of the Repair-Café, so it can be
    either a Reparateur or an Organisator. Organisators have access to the private
    data form the guests and must be nominated by an admin.
    """
    organisator = Organisator.objects.filter(mail=user.email).first()
    if not organisator:
        # no organisator, create or update reparateur
        reparateur = Reparateur.objects.filter(mail=user.email).first()
        if not reparateur:
            # create new reparateur
            reparateur = Reparateur(
                name=user.username,
                mail=user.email,
            )
            reparateur.save()
        else:
            # update name of existing reparateur
            reparateur.name = user.username
            reparateur.save()
    else:
        # update name of organisator
        organisator.name = user.username
        organisator.save()


class OneTimeLoginBackend(ModelBackend):
    """
    OneTimeLoginBackend implements a login using a onetime secret.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
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
        logger.info('Create user %s' % user.email)

        fallback_name = generate_username(user.email)
        try:
            user.username = claims.get('preferred_username', fallback_name)
            user.save()
        except Exception as exception:
            logger.error(exception)
            logger.warning(
                'Update username failed! Using fallback name %s.' % fallback_name)
            user.username = fallback_name
            user.save()

        logger.debug(f'Updated username {user.username}')

        create_repapp_user(user)

        return user

    def update_user(self, user, claims):
        logger.debug(f'Update user {user.email} ({user.username})')
        try:
            user.username = claims.get(
                'preferred_username', generate_username(user.email))
            user.save()
        except Exception as exception:
            logger.error(exception)

        create_repapp_user(user)

        return user

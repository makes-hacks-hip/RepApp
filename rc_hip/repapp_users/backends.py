import unicodedata
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from repapp.models import Organisator, Reparateur


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


def generate_username(email):
    # Using Python 3 and Django 1.11+, usernames can contain alphanumeric
    # (ascii and unicode), _, @, +, . and - characters. So we normalize
    # it and slice at 150 characters.
    return unicodedata.normalize('NFKC', email)[:150]


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


class KeycloakOIDCAB(OIDCAuthenticationBackend):
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

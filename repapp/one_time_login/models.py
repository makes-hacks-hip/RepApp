"""
Data models for the one time login feature.
"""

import django.utils.timezone
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class OneTimeLogin(models.Model):
    """
    A one time login (otl) is a secret which can be used once to login a user.
    """
    secret = models.CharField(max_length=200, verbose_name=_(
        "Secret"), unique=True, null=False)
    url = models.CharField(max_length=200, verbose_name=_("URL"))
    created = models.DateField(verbose_name=_(
        "Creation date"), default=django.utils.timezone.now)
    login_used = models.BooleanField(
        verbose_name=_("Was the login used?"), default=False)
    login_date = models.DateField(verbose_name=_("Login date"), null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, verbose_name=_("User"))

    class Meta:
        verbose_name = _('One time login')
        verbose_name_plural = _('One time logins')

    def __str__(self):
        return f'One time login for {self.user}'

    def get_absolute_url(self):
        return reverse('one_time_login:login', args=[self.secret])

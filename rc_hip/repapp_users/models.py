from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_("eMail Adresse"))

    class Meta:
        verbose_name = _('Benutzer')
        verbose_name_plural = _('Benutzer')

    def __str__(self):
        return f'{self.email}'

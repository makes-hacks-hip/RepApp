"""
This module implements the models of RepApp.
"""
import django.utils.timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class Cafe(models.Model):
    """
    A Cafe is a "Repair-Café event.
    """
    location = models.CharField(
        max_length=200, verbose_name=_("Ort"))
    address = models.CharField(
        max_length=200, verbose_name=_("Adresse"))
    event_date = models.DateField(verbose_name=_("Datum"))

    class Meta:
        verbose_name = _('Repair-Café')
        verbose_name_plural = _('Repair-Cafés')

    def __str__(self):
        return f'Repair-Café am {self.event_date} (Ort: {self.location})'


class Reparateur(models.Model):
    """
    A Reparateur is a member of the Repair-Café who supports guests with fixing their devices.
    """
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    mail = models.CharField(max_length=200, verbose_name=_("eMail"))

    class Meta:
        verbose_name = _('Reparateur')
        verbose_name_plural = _('Reparateure')

    def __str__(self):
        return f'Reparateur {self.name} (eMail: {self.mail})'


class Organisator(models.Model):
    """
    A Organisator is a member of the Repair-Café who arranges repair appointments with guests.
    """
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    mail = models.CharField(max_length=200, verbose_name=_("eMail"))

    class Meta:
        verbose_name = _('Organisator')
        verbose_name_plural = _('Organisatoren')

    def __str__(self):
        return f'Organisator {self.name} (eMail: {self.mail})'


class Guest(models.Model):
    """
    A guest is a owner of a broken device who wants support in context of a Repair-Café.
    """
    identifier = models.CharField(max_length=200, verbose_name=_("ID"))
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    phone = models.CharField(max_length=200, verbose_name=_("Telefonnummer"))
    residence = models.CharField(max_length=200, verbose_name=_("Wohnort"))
    mail = models.CharField(max_length=200, verbose_name=_("eMail"))

    class Meta:
        verbose_name = _('Gast')
        verbose_name_plural = _('Gäste')

    def __str__(self):
        return f'Gast {self.name} (eMail: {self.mail})'


def device_directory_path(instance, filename):
    """
    device_directory_path generates a device-specific storage path for file uploads.
    """
    return f'device_{instance.identifier}/{filename}'


class Device(models.Model):
    """
    A Device is a broken device owned by a guest which shall be repaired during a Repair-Café.
    """
    identifier = models.CharField(max_length=200, verbose_name=_("ID"))
    device = models.CharField(max_length=200, verbose_name=_("Art des Geräts"))
    manufacturer = models.CharField(
        max_length=200, verbose_name=_("Hersteller & Modell/Typ"))
    error = models.TextField(verbose_name=_("Fehlerbeschreibung"))
    follow_up = models.BooleanField(verbose_name=_("Folgetermin"))
    device_picture = models.FileField(
        upload_to=device_directory_path, null=True, verbose_name=_("Foto vom Gerät"))
    type_plate_picture = models.FileField(
        upload_to=device_directory_path, null=True, verbose_name=_("Foto vom Typenschild"))
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, null=True, verbose_name=_("Gast"))
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, null=False, verbose_name=_("Repair-Café"))
    confirmed = models.BooleanField(verbose_name=_("Bestätigung gesendet?"))
    date = models.DateField(verbose_name=_(
        "Erstellungsdatum"), default=django.utils.timezone.now)

    class Meta:
        verbose_name = _('Gerät')
        verbose_name_plural = _('Geräte')

    def __str__(self):
        return f'Gerät {self.device}'


class Appointment(models.Model):
    """
    A Appointment is a match of a broken Device and a Reparateur during a Repair-Café
    with a defined time slot.
    """
    time = models.TimeField(verbose_name=_("Zeit"))
    confirmed = models.BooleanField(verbose_name=_("bestätigt"))
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, verbose_name=_("Repair-Café"))
    reparateur = models.ForeignKey(
        Reparateur, on_delete=models.CASCADE, verbose_name=_("Reparateur"))
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, null=True, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Termin')
        verbose_name_plural = _('Termine')

    def __str__(self):
        return f'Termin {self.cafe.event_date} {self.time} für Gerät {self.device.device}'


class Question(models.Model):
    """
    A Question is a request for information form a Organisator or a Reparateur for a Device.
    """
    question = models.TextField(verbose_name=_("Frage"))
    answer = models.TextField(verbose_name=_("Antwort"))
    date = models.DateField(verbose_name=_(
        "Erstellungsdatum"), default=django.utils.timezone.now)
    organisator = models.ForeignKey(
        Organisator, on_delete=models.CASCADE, null=True, verbose_name=_("Organisator"))
    reparateur = models.ForeignKey(
        Reparateur, on_delete=models.CASCADE, null=True, verbose_name=_("Reparateur"))
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Frage')
        verbose_name_plural = _('Fragen')

    def __str__(self):
        return f'Frage vom {self.date} zum Gerät {self.device.device}'


class Candidate(models.Model):
    """
    A Candidate is a match of a broken Device and a Repair-Café without a fixed timeslot
    or pre-assigned Reparateur.
    """
    confirmed = models.BooleanField(verbose_name=_("bestätigt"))
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, verbose_name=_("Repair-Café"))
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, null=True, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Kandidat')
        verbose_name_plural = _('Kandidaten')

    def __str__(self):
        return f'Kandidat {self.cafe.event_date} für Gerät {self.device.device}'


class CustomUser(AbstractUser):
    """
    Custom user object with unique email.
    """
    email = models.EmailField(unique=True, verbose_name=_("eMail Adresse"))

    class Meta:
        verbose_name = _('Benutzer')
        verbose_name_plural = _('Benutzer')

    def __str__(self):
        return f'{self.email}'


class OneTimeLogin(models.Model):
    """
    A OneTimeLogin is a secret which can be used once to login a user.
    """
    secret = models.CharField(max_length=200, verbose_name=_(
        "secret"), unique=True, null=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, verbose_name=_("Benutzer"))
    url = models.CharField(max_length=200, verbose_name=_("URL"))
    created = models.DateField(verbose_name=_(
        "Erstellungsdatum"), default=django.utils.timezone.now)
    login_used = models.BooleanField(
        verbose_name=_("Login benutzt?"), default=False)
    login_date = models.DateField(verbose_name=_(
        "Login Datum"), null=True)

    class Meta:
        verbose_name = _('Einmal-Login')
        verbose_name_plural = _('Einmal-Login')

    def __str__(self):
        return f'Einmal-Login {self.user.email}'


class Message(models.Model):
    """
    A Message is a request from a guest.
    """
    message = models.TextField(verbose_name=_("Nachricht"))
    answer = models.TextField(verbose_name=_("Antwort"))
    date = models.DateField(verbose_name=_(
        "Erstellungsdatum"), default=django.utils.timezone.now)
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, null=True, verbose_name=_("Gast"))

    class Meta:
        verbose_name = _('Nachricht')
        verbose_name_plural = _('Nachrichten')

    def __str__(self):
        return f'Nachricht vom {self.date} von {self.guest.mail}'

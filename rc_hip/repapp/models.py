"""
This module implements the models of RepApp.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cafe(models.Model):
    """
    A Cafe is a "Repair-Café event.
    """
    location = models.CharField(
        max_length=200, verbose_name=_("Ort"))
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


class Device(models.Model):
    """
    A Device is a broken device owned by a guest which shall be repaired during a Repair-Café.
    """
    identifier = models.CharField(max_length=200, verbose_name=_("ID"))
    device = models.CharField(max_length=200, verbose_name=_("Gerät"))
    error = models.TextField(verbose_name=_("Fehler"))
    follow_up = models.BooleanField(verbose_name=_("Folgetermin"))
    guest_id = models.ForeignKey(
        Guest, on_delete=models.CASCADE, null=True, verbose_name=_("Gast"))

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
    cafe_id = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, verbose_name=_("Repair-Café"))
    reparateur_id = models.ForeignKey(
        Reparateur, on_delete=models.CASCADE, verbose_name=_("Reparateur"))
    device_id = models.ForeignKey(
        Device, on_delete=models.CASCADE, null=True, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Termin')
        verbose_name_plural = _('Termine')

    def __str__(self):
        return f'Termin {self.cafe_id.event_date} {self.time} für Gerät {self.device_id.device}'


class Candidate(models.Model):
    """
    A Candidate is a match of a broken Device and a Repair-Café without a fixed timeslot
    or pre-assigned Reparateur.
    """
    confirmed = models.BooleanField(verbose_name=_("bestätigt"))
    cafe_id = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, verbose_name=_("Repair-Café"))
    device_id = models.ForeignKey(
        Device, on_delete=models.CASCADE, null=True, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Kandidat')
        verbose_name_plural = _('Kandidaten')

    def __str__(self):
        return f'Kandidat {self.cafe_id.event_date} für Gerät {self.device_id.device}'


class Question(models.Model):
    """
    A Question is a request for information form a Organisator or a Reparateur for a Device.
    """
    question = models.TextField(verbose_name=_("Frage"))
    answer = models.TextField(verbose_name=_("Antwort"))
    date = models.DateField(verbose_name=_("Erstellungsdatum"))
    organisator_id = models.ForeignKey(
        Organisator, on_delete=models.CASCADE, null=True, verbose_name=_("Organisator"))
    reparateur_id = models.ForeignKey(
        Reparateur, on_delete=models.CASCADE, null=True, verbose_name=_("Reparateur"))
    device_id = models.ForeignKey(
        Device, on_delete=models.CASCADE, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Frage')
        verbose_name_plural = _('Fragen')

    def __str__(self):
        return f'Frage vom {self.date} zum Gerät {self.device_id.device}'

from django.db import models
from django.utils.translation import gettext_lazy as _


class Cafe(models.Model):
    location = models.CharField(
        max_length=200, verbose_name=_("Ort"))
    event_date = models.DateField(verbose_name=_("Datum"))

    class Meta:
        verbose_name = _('Repair-Café')
        verbose_name_plural = _('Repair-Cafés')

    def __str__(self):
        return f'Repair-Café am {self.event_date} (Ort: {self.location})'


class Reparateur(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    mail = models.CharField(max_length=200, verbose_name=_("eMail"))

    class Meta:
        verbose_name = _('Reparateur')
        verbose_name_plural = _('Reparateure')

    def __str__(self):
        return f'Reparatuer {self.name} (eMail: {self.mail})'


class Organisator(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    mail = models.CharField(max_length=200, verbose_name=_("eMail"))

    class Meta:
        verbose_name = _('Organisator')
        verbose_name_plural = _('Organisatoren')

    def __str__(self):
        return f'Organisator {self.name} (eMail: {self.mail})'


class Device(models.Model):
    identifier = models.CharField(max_length=200, verbose_name=_("ID"))
    owner = models.CharField(max_length=200, verbose_name=_("Besitzer"))
    mail = models.CharField(max_length=200, verbose_name=_("eMail"))
    device = models.CharField(max_length=200, verbose_name=_("Gerät"))
    error = models.TextField(verbose_name=_("Fehler"))
    follow_up = models.BooleanField(verbose_name=_("Folgetermin"))

    class Meta:
        verbose_name = _('Gerät')
        verbose_name_plural = _('Geräte')

    def __str__(self):
        return f'Gerät {self.device} von {self.owner} (eMail: {self.mail})'


class Appointment(models.Model):
    time = models.TimeField(verbose_name=_("Zeit"))
    confirmed = models.BooleanField(verbose_name=_("bestätigt"))
    cafeid = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, verbose_name=_("Repair-Café"))
    reparateurid = models.ForeignKey(
        Reparateur, on_delete=models.CASCADE, verbose_name=_("Reparateur"))
    deviceid = models.ForeignKey(
        Device, on_delete=models.CASCADE, null=True, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Termin')
        verbose_name_plural = _('Termine')

    def __str__(self):
        return f'Termin {self.cafeid.event_date} {self.time} für Gerät {self.deviceid.device} von {self.deviceid.owner}'


class Question(models.Model):
    question = models.TextField(verbose_name=_("Frage"))
    answer = models.TextField(verbose_name=_("Antwort"))
    date = models.DateField(verbose_name=_("Erstellungsdatum"))
    organisatorid = models.ForeignKey(
        Organisator, on_delete=models.CASCADE, null=True, verbose_name=_("Organisator"))
    reparateurid = models.ForeignKey(
        Reparateur, on_delete=models.CASCADE, null=True, verbose_name=_("Reparateur"))
    deviceid = models.ForeignKey(
        Device, on_delete=models.CASCADE, verbose_name=_("Gerät"))

    class Meta:
        verbose_name = _('Frage')
        verbose_name_plural = _('Fragen')

    def __str__(self):
        return f'Frage vom {self.date} zum Gerät {self.deviceid.device}'

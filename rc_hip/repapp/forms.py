"""
Django forms for RepApp.
"""
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.layout import Field


EMPTY_VALUES = (None, '')


class HoneypotWidget(forms.TextInput):
    """
    This widget shows a by CSS hidden input field. If this form gets manipulated
    by a bot the form is rejected.
    """
    is_hidden = True

    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment
        super(HoneypotWidget, self).__init__(attrs, *args, **kwargs)
        if not 'class' in self.attrs:
            self.attrs['style'] = 'display:none'

    def render(self, *args, **kwargs):
        value = super(HoneypotWidget, self).render(*args, **kwargs)
        if self.html_comment:
            value = '<!-- %s -->' % value
        return value


class HoneypotField(forms.Field):
    """
    This widget implements a simple honey pot field as spam protection.
    """
    widget = HoneypotWidget

    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value
        raise ValidationError('Anti-spam field changed in value.')


class RegisterDevice(forms.Form):
    """
    Form for registering a device for a repair cafe.
    """
    mail = forms.EmailField(
        label="eMail Adresse",
        help_text="Diese eMail-Adresse wird für Aktualisierungen"
        " zur Anfrage verwendet.",
        max_length=200)
    device = forms.CharField(
        label="Art des Geräts",
        help_text="z.B. Küchenmaschine, Smartphone, Stehlampe, Drucker, ...",
        max_length=200
    )
    manufacturer = forms.CharField(
        label="Hersteller & Modell/Typ",
        max_length=200
    )
    error = forms.CharField(
        label="Fehlerbeschreibung",
        help_text="Beschreiben Sie hier das Problem ihres Gerätes.",
        widget=forms.Textarea
    )
    device_picture = forms.FileField(
        label="Foto vom Gerät", required=False
    )
    type_plate_picture = forms.FileField(
        label="Foto vom Typenschild", required=False
    )
    follow_up = forms.BooleanField(
        label="Folgetermin",
        help_text="Kreuzen Sie diese Kästchen an wenn sie mit diesem Gerät "
        "bereits bei einem Repair-Café Termin waren.",
        required=False
    )
    confirm_repair = forms.BooleanField(
        label="Informationen zur Reparaturabwicklung",
        help_text="Ich bin mit den <a href="
        "\"https://www.repaircafe-hilpoltstein.de/fileadmin/repaircafe-hilpoltstein/images/"
        "repaircafe-hilpoltstein.de/docs/Infos_Reparatur-Abwicklung_v2_2023-02.pdf\">"
        "Allgemeinen Bedingungen zur Reparaturabwicklung</a> einverstanden.",
        required=True
    )
    confirm_data = forms.BooleanField(
        label="Datenschutz",
        help_text=" Ich bin mit der Erhebung, Verarbeitung und Speicherung meiner Daten für "
        "die Bearbeitung meiner Anfrage gemäß der "
        "<a href=\"https://www.repaircafe-hilpoltstein.de/impressum#c1375\">"
        "Datenschutzerklärung</a> einverstanden.",
        required=True
    )
    accept_agb = HoneypotField(label="")


class RegisterGuest(forms.Form):
    """
    Form for registering new guests.
    """
    name = forms.CharField(
        label="Name",
        max_length=200
    )
    phone = forms.CharField(
        label="Telefonnummer",
        max_length=200,
        help_text="Diese Telefonnummer wird für Rückfragen verwendet."
    )
    residence = forms.CharField(
        label="Wohnort",
        max_length=200
    )
    accept_agb = HoneypotField(label="")


class CreateCafe(forms.Form):
    """
    Form for creating new Repair-Cafés.
    """
    location = forms.CharField(
        label="Ort",
        max_length=200,
        help_text="Name des Orts, z.B. AWO."
    )
    address = forms.CharField(
        label="Adresse",
        max_length=200,
        help_text="Straße, Hausnummer und Ortsname."
    )
    event_date = forms.DateField(
        label="Veranstaltungsdatum"
    )

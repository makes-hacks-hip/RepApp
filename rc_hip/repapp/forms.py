from django import forms


class RegisterDevice(forms.Form):
    mail = forms.EmailField(
        label="eMail Adresse",
        help_text="Diese eMail-Adresse wird für Aktualisierungen"
        " zur Anfrage verwendet.",
        max_length=200)
    device = forms.CharField(
        label="Gerätebezeichnung",
        help_text="Bitte geben Sie den Hersteller und die"
        " Gerätebezeichnung an.",
        max_length=200
    )
    error = forms.CharField(
        label="Fehlerbeschreibung",
        help_text="Beschreiben Sie hier das Problem ihres Gerätes.",
        widget=forms.Textarea
    )
    follow_up = forms.BooleanField(
        label="Folgetermin",
        help_text="Klicken Sie dieses Kästchen an wenn sie mit diesem"
        " Gerät bereits bei einem Repair-Café waren.",
        required=False
    )


class RegisterGuest(forms.Form):
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

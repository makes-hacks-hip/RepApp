from django import forms


class RegisterDevice(forms.Form):
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
        label="Foto vom Gerät ", required=False
    )
    type_plate_picture = forms.FileField(
        label="Foto vom Typenschild ", required=False
    )
    follow_up = forms.BooleanField(
        label="Folgetermin",
        help_text="Kreuzen Sie diese Kästchen an wenn sie mit diesem Gerät bereits bei einem Repair-Café Termin waren.",
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

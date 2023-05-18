# Ansichten

## Landing Page: Repair-Cafés (S1)

URL: /

Name: index

Sicherheit: Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

Diese Seite zeigt eine Liste der zukünftigen Repair-Café Termine. 
Sie enthält pro Repair-Café einen Link um ein Gerät für dieses Repair-Café anzumelden.

## Gerät anmelden (S2)

URL: cafe/int:cafe/

Name: register_device

Sicherheit: Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

Diese Seite zeigt das Formular zum anmelden der Geräte.
Das Formular hat die Felder `eMail-Adresse`, `Art des Geräts`, `Hersteller & Modell/Typ`, `Fehlerbeschreibung`, `Foto vom Gerät`, `Foto vom Typenschild`, ein Kontrollkästchen `Folgetermin`, ein Kontrollkästchen `Informationen zur Reparaturabwicklung`, ein Kontrollkästchen `Datenschutz` und einen Knopf `Absenden` zum senden des Formulars.

Das Repair-Café zu dem die Anmeldung gehört ist über eine ID in der URL der Seite festgelegt.

Falls die eMail Adresse zu einem bekannten Gast gehört, wird beim absenden des Formulars eine eMail-Benachrichtigung and die Organisatoren und  Bestätigung an den Gast gesendet.

## Gast anmelden (S3)

URL: cafe/int:cafe/device/str:device_identifier/mail/str:mail/

Name: register_guest

Sicherheit: Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

Diese Seite zeigt das Formular zum anmelden eines neuen Gastes.
Das Formular hat die Felder `Name`, `Telefon`, `Wohnort` und einen Knopf `Absenden` zum senden des Formulars.

Die eMail-Adresse und das Gerät zu dem die Gast-Kontaktdaten gehören ist über IDs in der URL der Seite festgelegt.

Beim absenden des Formulars eine eMail-Benachrichtigung and die Organisatoren und  Bestätigung an den Gast gesendet.

## Anmeldung bestätigt (S7)

URL: cafe/int:cafe/device/str:device_identifier/confirm/

Name: register_device_final

Sicherheit: Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

Die Seite Anmeldung bestätigt zeigt einen Hinweis dass die Anmeldung des Gerätes erfolgreich abgeschlossen wurde.

Die Geräte ID ist in der URL der Seite festgelegt.

## Geräte Detailseite (S5)

URL: device/str:device_identifier/

Name: view_device

Sicherheit: Diese Seite ist für alle Mitarbeiter und den Gast der das Gerät angemeldet hat erreichbar.

Die Geräte Detailseite zeigt die Informationen `Art des Geräts`, `Hersteller & Modell/Typ`, `Fehlerbeschreibung`, `Foto vom Gerät`, `Foto vom Typenschild` und `Folgetermin` an.

Das Gerät ist über IDs in der URL der Seite festgelegt.

## Gast Detailseite (S6)

URL: guest/profile/

Name: guest_profile

Sicherheit: Die Seite enthält persönliche Daten und ist nur für den Gast zu dem sie gehört erreichbar.

Die Gast Detailseite hat die Felder `Name`, `eMail`, `Telefon` und `Wohnort` die mit den Angaben des Gastes ausgefüllt sind.
Weiter enthält die Seite einen Knopf `Aktualisieren` der das Formular absendet.
Die Ansicht enthält auch eine Liste mit Links zu allen Geräten die der Gast angemeldet hat.

Der Gast ist über den angemeldeten Benutzer festgelegt.

# Projekt RepApp

RepApp ist eine Web App um Reparaturen im Rahmen eines Repair-Cafés zu organisieren.

## Benutzer

### Gast

Ein Gast ist ein Gerätebesitzer der ein oder mehrere Geräte zur Reparatur anmelden möchte.

### Reparateur

Ein Reparateur ist ein Mitglied des Repair-Cafés das die Gäste bei der Reparatur ihrer Geräte unterstützt.

### Organisator

Ein Organisator ist Mitglied des Repair-Cafés das die Termine mit den Gästen organisiert und die Reparateure zu den Geräten zuordnet.

## Anwendungsfälle

### Gast

- [x] Als Gast möchte ich einen Termin für eine Reparatur vereinbaren. (A1)
- [x] Als Gast möchte ich eine Bestätigung für eine Reparaturanfrage bekommen. (A2)
- [ ] Als Gast möchte ich eine Terminbenachrichtigung oder eine Absage bekommen. (A3)
- [ ] Als Gast möchte ich mein angemeldetes Gerät und dessen Status einsehen können. (A4)
- [ ] Als Gast möchte ich Rückfragen zum Gerät empfangen und diese beantworten können. (A5)
- [ ] Als Gast möchte ich ein Gerät für eine Folgereparatur anmelden können. (A6)
- [ ] Als Gast möchte ich meine Daten ansehen können. (A21)
- [ ] Als Gast möchte ich meine Daten löschen können. (A22)
- [ ] Als Gast möchte ich eine Geräteanmeldung löschen können. (A23)

### Reparateur

- [ ] Als Reparateur möchte ich die angemeldeten Geräte ansehen können. (A7)
- [ ] Als Reparateur möchte ich mir ein angemeldetes Gerät zuordnen können. (A8)
- [ ] Als Reparateur möchte ich ein angemeldetes Gerät ablehnen können. (A9)
- [ ] Als Reparateur möchte ich Rückfragen zum Gerät stellen können. (A10)
- [ ] Als Reparateur möchte ich eine Benachrichtigung bekommen wenn eine Rückfrage beantwortet wird. (A11)
- [ ] Als Reparateur möchte ich eine Benachrichtigung bekommen wenn mir ein Gerät zugeordnet wird. (A12)
- [ ] Als Reparateur möchte ich mich für ein Repair-Café anmelden können. (A13)
- [ ] Als Reparateur möchte ich mich für ein Repair-Café abmelden können. (A14)
- [ ] Als Reparateur möchte ich benachrichtigt werden wenn ein Gast eine mir zugeordnete Geräteanmeldung löscht. (A25)

### Organisator

- [x] Als Organisator möchte ich benachrichtigt werden wenn ein Gast ein Gerät anmeldet. (A25)
- [ ] Als Organisator möchte ich ein Repair-Café anlegen können. (A15)
- [ ] Als Organisator möchte ich die Geräte einsehen können. (A16)
- [ ] Als Organisator möchte ich eine Rückfrage zu einem Geräte stellen können. (A17)
- [ ] Als Organisator möchte ich ein Geräte ablehnen können. (A18)
- [ ] Als Organisator möchte ich ein Geräte zu einem Termin zuordnen können. (A19)
- [ ] Als Organisator möchte ich einen Reparateur zu einem Termin zuordnen können. (A20)
- [ ] Als Organisator möchte ich benachrichtigt werden wenn ein Gast eine Geräteanmeldung löscht. (A24)

## Daten

### Cafe

Ein Cafe ist ein Repair-Café Termin.

Attribute:

- Datum: Datum der Veranstaltung
- Ort: Beschreibung wo das Repair-Café stattfindet

Annahmen:

- Ein Repair-Café beginnt um 13:00 Uhr.
- Ein Repair-Café hat drei aufeinanderfolgende Zeitslots pro Reparateur mit je einer Stunde

### Reparateur

Ein Reparateur ist ein Mitglied des Repair-Cafés das Gäste bei der Reparatur ihrer Geräte unterstützt.

Attribute:

- Name: Name des Reparateurs
- Mail: eMail-Adresse für Benachrichtigungen

Annahmen:

- Reparateure sind immer verfügbar, d.h. Zeitslots für jeden Reparateur werden zu einem neuen Repair-Café Termin automatisch hinzugefügt.
- Reparateure können alles reparieren. Geräte Kategorien, Skills, ... werden im Moment nicht berücksichtigt. 

### Organisator

Ein Organisator ist ein Mitglied des Repair-Cafés das Reparaturtermine mit den Gästen vereinbart.

Attribute:

- Name: Name des Organisators
- Mail: eMail-Adresse für Benachrichtigungen

### Gast

Ein Gast ist ein Gerätebesitzer, der ein Gerät zur Reparatur anmeldet.

Attribute:

- Name: Name des Gastes
- Telefon: Festnetz oder Mobilnummer des Gastes
- Wohnort: Wohnort des Gastes
- Mail: eMail-Adresse des Gastes für Benachrichtigungen
- Bestätigt: Ein boolesches Flag das anzeigt ob der Gast seine eMail-Adresse bestätigt hat.

Technische Attribute:

- Identifier: SHA256 Hash aus Name + Wohnort + Timestamp

### Gerät

Ein Gerät ist ein defekter Gegenstand der im Rahmen eines Repair-Cafés repariert werden soll.

Attribute:

- Gerät: Bezeichnung des Geräts
- Fehler: Beschreibung des Defekts
- Folgetermin: Boolesches Flag das anzeigt ob es sich um einen Folgetermin handelt.
- Bestätigt: Ein boolesches Flag das anzeigt ob der Gast die Greäteanmeldung bestätigt hat.

Technische Attribute:

- Identifier: SHA256 Hash aus Gerät + Gast + Timestamp
- Geheimnis: SHA256 Hash aus Gerät + Gast + Timestamp + Zufallszahl
- Gast: Referenz zum Gast der das Gerät besitzt

### Termin

Ein Termin ist eine Zuordnung von einem Gerät zu einem Zeitslot der Repair-Café Veranstaltung und einem Reparateur.
Ein Termin ist bestätigt, wenn eine Organisator eine Termineinladung gesendet hat und er Gast diese bestätigt hat. 

Attribute:

- Uhrzeit: Uhrzeit des Termins
- Betätigt: Boolesches Flag. True wenn die Einladung vom Gast bestätigt wurde.

Technische Attribute:

- Cafe: Referenz zum Cafe
- Reparateur: Referenz um Reparateur oder NULL
- Gerät: Referenz zum Gerät

### Frage

Eine Frage ist eine Rückfrage nach mehr Informationen zu einem Gerät, erstellt von einem Organisator oder einem Reparateur.

Attribute:

- Frage: Frage zum Gerät oder Defekt
- Antwort: Antwort des Gastes
- Datum: Datum der Erstellung der Rückfrage

Technische Attribute:

- Organisator: Referenz zum Organisator oder NULL
- Reparateur: Referenz zum Reparateur oder NULL
- Gerät: Referenz zum Gerät

### Kandidat

Ein Kandidat ist ein Geräte ohne festen Termin.
Diese Geräte werden von den Gästen zu Beginn des Repair-Café gebracht und am Ende abgeholt.
Falls ein Reparateur Zeit hat kann er eines dieser Geräte reparieren.

- Bestätigt: Boolesches Flag. True wenn die Einladung vom Gast bestätigt wurde.

Technische Attribute:

- Cafe: Referenz zum Cafe
- Gerät: Referenz zum Gerät

## Ansichten

### Landing Page: Repair-Cafés (S1)

URL: /

Name: index

Diese Seite zeigt eine Liste der zukünftigen Repair-Café Termine. 
Sie enthält pro Repair-Café einen Knopf um ein Gerät für dieses Repair-Café anzumelden.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Gerät anmelden (S2)

URL: cafe/<int:cafe>/

Name: register_device

Diese Seite zeigt das Formular zum anmelden der Geräte.
Das Formular hat die Felder `eMail-Adresse`, `Gerätebezeichnung`, `Fehlerbeschreibung`, eine Kontrollkästchen `Folgetermin` und einen Knopf `Absenden` zum senden des Formulars.

Das Repair-Café zu dem die Anmeldung gehört ist über eine ID in der URL der Seite festgelegt.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Gast anmelden (S3)

URL: cafe/<int:cafe>/device/<str:deviceentifier>/<str:mail>/

Name: register_guest

Diese Seite zeigt das Formular zum anmelden eines neuen Gastes.
Das Formular hat die Felder `Name`, `Telefon`, `Wohnort` und einen Knopf `Absenden` zum senden des Formulars.

Die eMail-Adresse und das Gerät zu dem die Gast-Kontaktdaten gehören ist über IDs in der URL der Seite festgelegt.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Bestätigung gesendet (S4)

URL: cafe/<int:cafe>/device/<str:deviceentifier>/guest/<str:guestentifier>/

Name: register_device_final

Die Seite Bestätigung gesendet zeigt einen Hinweis dass eine eMail gesendet wurde und die Anmeldung des Gerätes durch einen Klick auf einen Link in der eMail bestätigt werden muss.

Die eMail-Bestätigung wird während des Aufrufs dieser Seite gesendet.

Das Repair-Café, der Gast und das Gerät sind über IDs in der URL der Seite festgelegt.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.


### Anmeldung bestätigt (S7)

URL: confirm/<str:deviceentifier>/code/<str:device_secret>

Name: register_device_confirm

Die Seite Anmeldung bestätigt zeigt einen Hinweis dass die Anmeldung des Gerätes erfolgreich abgeschlossen wurde.

Die eMail-Benachrichtigung and die Organisatoren wird während des Aufrufs dieser Seite gesendet.

Die Geräte ID ist in der URL der Seite festgelegt.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Geräte Detailseite (S5)

URL: device/<str:deviceentifier>

Name: view_device

Die Geräte Detailseite zeigt die Informationen `Gerätebezeichnung`, `Fehlerbeschreibung` und `Folgetermin` an.

Das Gerät ist über IDs in der URL der Seite festgelegt.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Gast Detailseite (S6)

Die Gast Detailseite hat die Felder `Name`, `eMail`, `Telefon` und `Wohnort` die mit den Angaben des Gastes ausgefüllt sind.
Weiter enthält die Seite einen Knopf `Aktualisieren` der das Formular absendet.
Die Ansicht enthält auch eine Liste mit Links zu allen Geräten die der Gast angemeldet hat.

Der Gast ist über IDs in der URL der Seite festgelegt.

#### Sicherheit

Die Seite enthält persönliche Daten und ist nur nach Anmeldung erreichbar.

## Abläufe

### Anmeldung eines defekten Gerätes

#### Variante: Neuer Gast

Als neuer Gast der ein defekten Geräte anmelden möchte,

- gehe ich auf die Seite (S1) der Repair-Café Termine. Dort klicke ich auf `Gerät anmelden` bei dem richtigen Repair-Café Termin. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S2) enthält ein Formular mit den Feldern `eMail-Adresse`, `Gerätebezeichnung` und `Fehlerbeschreibung` und eine Kontrollkästchen `Folgetermin`. Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S3) enthält ein Formular mit den Feldern `Name`, `Telefon` und `Wohnort`. Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`.  Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S4) weißt mich darauf hin dass eine eMail gesendet wurde und ich die Anmeldung über einen Klick in der eMail bestätigen muss.
- In meinem eMail Posteingang finde ich eine Bestätigung der Geräteanmeldung die ebenfalls einen Link enthält um die Anmeldung zu bestätigen. Ein Klick auf diesen Link bringt mich auf die Seite Anmeldung bestätigt (S7).

#### Variante: Bekannter Gast (existierende eMail Adresse)

Als bekannter Gast der ein defekten Geräte anmelden möchte,

- gehe ich auf die Seite (S1) der Repair-Café Termine. Dort klicke ich auf `Gerät anmelden` bei dem richtigen Repair-Café Termin. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S2) enthält ein Formular mit den Feldern `eMail-Adresse`, `Gerätebezeichnung` und `Fehlerbeschreibung` und eine Kontrollkästchen `Folgetermin`. Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S4) weißt mich darauf hin dass eine eMail gesendet wurde und ich die Anmeldung über einen Klick in der eMail bestätigen muss.
- In meinem eMail Posteingang finde ich eine Bestätigung der Geräteanmeldung die ebenfalls einen Link enthält um die Anmeldung zu bestätigen. Ein Klick auf diesen Link bringt mich auf die Seite Anmeldung bestätigt (S7).

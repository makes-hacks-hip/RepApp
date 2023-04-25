# Projekt RepApp

RepApp ist eine Web App um Reparaturen im Rahmen eines Repair-Cafés zu organisieren.

## Benutzer

RepApp unterscheidet zwischen den folgenden Benutzer-Typen:

### Gast

Ein Gast ist ein Gerätebesitzer der ein oder mehrere Geräte zur Reparatur anmelden möchte.

### Reparateur

Ein Reparateur ist ein Mitglied des Repair-Cafés das die Gäste bei der Reparatur ihrer Geräte unterstützt.

### Organisator

Ein Organisator ist Mitglied des Repair-Cafés das die Termine mit den Gästen organisiert und die Reparateure zu den Geräten zuordnet.

## Anwendungsfälle

Die Anwendungsfälle sind in Meilensteine unterteilt.
Zu Meilenstein 1 (M1) gehören alle Anwendungsfälle die notwendig sind um RepApp "produktiv" für die Anmeldung von Geräten zu verwenden.

### Gast

- [x] M1: Als Gast möchte ich einen Termin für eine Reparatur vereinbaren. (A1)
- [x] M1: Als Gast möchte ich eine Bestätigung für eine Reparaturanfrage bekommen. (A2)
- [ ] M1: Als Gast möchte ich eine Terminbenachrichtigung oder eine Absage bekommen. (A3)
- [ ] M1: Als Gast möchte ich Rückfragen zum Gerät empfangen und diese beantworten können. (A5)
- [ ] M1: Als Gast möchte ich Fragen ans Repair-Café stellen können. (A26)
- [ ] M1: Als Gast möchte ich ausschließlich per eMail mit dem System interagieren können. (A30)
- [ ] M1: Als Gast möchte per eMail Fragen ans Team stellen können. (A33)
- [ ] M1: Als Gast möchte ich per eMail auf Rückfragen antworten können. (A34)
- [ ] M1: Als Gast möchte ich eine Termineinladung per eMail bestätigen können. (A35)

- [ ] Als Gast möchte ich mein angemeldetes Gerät und dessen Status einsehen können. (A4)
- [ ] Als Gast möchte ich ein Gerät für eine Folgereparatur anmelden können. (A6)
- [ ] Als Gast möchte ich meine Daten ansehen können. (A21)
- [ ] Als Gast möchte ich meine Daten löschen können. (A22)
- [ ] Als Gast möchte ich eine Geräteanmeldung löschen können. (A23)

### Reparateur

- [ ] M1: Als Reparateur möchte ich die angemeldeten Geräte ansehen können. (A7)
- [ ] M1: Als Reparateur möchte ich mir ein angemeldetes Gerät zuordnen können. (A8)
- [ ] M1: Als Reparateur möchte ich Rückfragen zum Gerät stellen können. (A10)
- [ ] M1: Als Reparateur möchte ich eine Benachrichtigung bekommen wenn eine Rückfrage beantwortet wird. (A11)
- [ ] M1: Als Reparateur möchte ich eine Benachrichtigung bekommen wenn mir ein Gerät zugeordnet wird. (A12)
- [ ] M1: Als Reparateur möchte ich mich für ein Repair-Café anmelden können. (A13)
- [ ] M1: Als Reparateur möchte ich mich für ein Repair-Café abmelden können. (A14)

- [ ] Als Reparateur möchte ich ein angemeldetes Gerät ablehnen können. (A9)
- [ ] Als Reparateur möchte ich benachrichtigt werden wenn ein Gast eine mir zugeordnete Geräteanmeldung löscht. (A25)

### Organisator

- [x] M1: Als Organisator möchte ich benachrichtigt werden wenn ein Gast ein Gerät anmeldet. (A25)
- [ ] M1: Als Organisator möchte ich ein Repair-Café anlegen können. (A15)
- [ ] M1: Als Organisator möchte ich die Geräte einsehen können. (A16)
- [ ] M1: Als Organisator möchte ich eine Rückfrage zu einem Geräte stellen können. (A17)
- [ ] M1: Als Organisator möchte ich ein Geräte ablehnen können. (A18)
- [ ] M1: Als Organisator möchte ich ein Geräte zu einem Termin zuordnen können. (A19)
- [ ] M1: Als Organisator möchte ich einen Reparateur zu einem Termin zuordnen können. (A20)
- [ ] M1: Als Organisator möchte ich ein Gerät bearbeiten können. (A28)
- [ ] M1: Als Organisator möchte ich ein Gerät absagen können, wenn der Gast mich informiert hat dass er nicht kommt. (A29)

- [ ] Als Organisator möchte ich benachrichtigt werden wenn ein Gast eine Geräteanmeldung löscht. (A24)
- [ ] Als Organisator möchte ich alle Daten exportieren können. (A31)
- [ ] Als Organisator möchte ich Geräte auf ein späteres Repair-Café verschieben können. (A32)

## Daten


### Benutzer

Ein Repapp-Benutzer erweitert den Standard-Benutzer um eine eindeutige eMail-Adresse, um diese als Identifikationsmerkmal verwenden zu können.

### Cafe

Ein Cafe ist ein Repair-Café Termin.

Attribute:

- Ort: Beschreibung wo das Repair-Café stattfindet
- Adresse: Adresse an der das Repair-Café stattfindet
- Datum: Datum der Veranstaltung

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

Technische Attribute:

- Identifier: SHA256 Hash aus Name + Wohnort + Timestamp
- Benutzer: Referenz zum Benutzer der für diesen Gast erstellt wurde.

### Gerät

Ein Gerät ist ein defekter Gegenstand der im Rahmen eines Repair-Cafés repariert werden soll.

Attribute:

- Erstellungsdatum: Datum an dem diese Gerät angemeldet wurde.
- Gerät: Bezeichnung des Geräts
- Hersteller: Hersteller des Geräts
- Fehler: Beschreibung des Defekts
- Folgetermin: Boolesches Flag das anzeigt ob es sich um einen Folgetermin handelt.
- Foto vom Gerät
- Foto vom Typenschild
- Bestätigung gesendet?: Ein boolesches Flag das anzeigt ob eine eMail als Anmeldebestätigung gesendet wurde.

Technische Attribute:

- Identifier: SHA256 Hash aus Gerät + Gast + Timestamp
- Gast: Referenz zum Gast der das Gerät besitzt
- Cafe: Referenz zum Repair-Café für das diese Gerät angemeldet ist

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
- Erstellungsdatum: Datum der Erstellung der Rückfrage

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

### Einmal-Login

Ein Einmal-Login ist ein Geheimnis das es einem Gast erlaubt sich einmalig damit anzumelden.

- Geheimnis: Geheimnis um den Gast zu identifizieren.
- URL: URL die nach der Anmeldung angezeigt werden soll.
- Erstellungsdatum: Datum an dem der Einmal-Login angelegt wurde.
- Login benutzt?: Boolesches Flag. True wenn der Einmal-Login bereits benutzt wurde.
- Login Datum: Datum an dem der Einmal-Login benutzt wurde, oder Datum der Erstellung, da das Feld aus technischen Gründen nicht leer sein kann.

Technische Attribute:

- Benutzer: Referenz zum Benutzer

### Nachricht

Eine Nachricht ist eine Anfrage von einem Gast.

- Nachricht: Anfrage des Gastes.
- Antwort: Antwort an den Gast.
- Erstellungsdatum: Datum an dem die Anfrage erstellt wurde.

Technische Attribute:

- Gast: Referenz zum Gast

## Anmelde Konzept

RepApp unterstützt pro Benutzer-Gruppe verschiedenen Anmelde-Konzepte.

## Gäste

Für Gäste wird automatsch ein Benutzerkonto angelegt, mit einem generierten, sicheren Passwort. Mit der eMail Adresse und dem Passwort kann ein Gast sich in der RepApp anmelden um seine Daten sehen und bearbeiten zu können.

### Einmal-Login

Für Gäste gibt es Einmal-Logins als Alternative. Ein Einmal-Login ist ein Geheimnis und eine Ziel-URL, das dem Gast in From eines Anmelde-Links in einer eMail mitgeteilt wird. Mit diesem Link kann der Gast sich einmalig anmelden, da das Geheimnis danach potentiell Dritten bekannt ist, z.B. über die Browser History.

Nach dem erfolgreichen Login wird der Gast automatisch zu der hinterlegten URL weitergeleitet. Dieser Mechanismus erlaubt es einem Gast "per Klick" Zugriff auf geschützte Daten zu geben.

Wenn ein Gast versucht den Einmal-Link nochmals zu verwenden, schlägt dies Fehl, und dem Gast wird automatisch ein neuer Einmal-Link per eMail mitgeteilt. Dies wird dem Gast auch über entsprechende Nachrichten mitgeteilt.

## Mitarbeiter

Der Login für Mitarbeiter ist nur über das Single-Sign-On der Repair-Cafés erlaubt (Keycloak), das mittels OIDC angebunden ist. Alle Mitarbeiter im Repair-Café haben dort bereits einen Benutzer, was zum einen sicherstellt dass es sich um einen Mitarbeiter handelt, und zum anderen auch die Veraltung der Benutzer in RepApp vereinfacht.

## Ansichten

### Landing Page: Repair-Cafés (S1)

URL: /

Name: index

Diese Seite zeigt eine Liste der zukünftigen Repair-Café Termine. 
Sie enthält pro Repair-Café einen Knopf um ein Gerät für dieses Repair-Café anzumelden.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Gerät anmelden (S2)

URL: cafe/int:cafe/

Name: register_device

Diese Seite zeigt das Formular zum anmelden der Geräte.
Das Formular hat die Felder `eMail-Adresse`, `Art des Geräts`, `Hersteller & Modell/Typ`, `Fehlerbeschreibung`, `Foto vom Gerät`, `Foto vom Typenschild`, ein Kontrollkästchen `Folgetermin`, ein Kontrollkästchen `Informationen zur Reparaturabwicklung`, ein Kontrollkästchen `Datenschutz` und einen Knopf `Absenden` zum senden des Formulars.

Das Repair-Café zu dem die Anmeldung gehört ist über eine ID in der URL der Seite festgelegt.

Die eMail-Benachrichtigung and die Organisatoren und die Bestätigung an den Gast wird beim absenden des Formulars gesendet, falls die eMail Adresse zu einem bekannten Gast gehört.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Gast anmelden (S3)

URL: cafe/int:cafe/device/str:device_identifier/mail/str:mail/

Name: register_guest

Diese Seite zeigt das Formular zum anmelden eines neuen Gastes.
Das Formular hat die Felder `Name`, `Telefon`, `Wohnort` und einen Knopf `Absenden` zum senden des Formulars.

Die eMail-Adresse und das Gerät zu dem die Gast-Kontaktdaten gehören ist über IDs in der URL der Seite festgelegt.

Die eMail-Benachrichtigung and die Organisatoren und die Bestätigung an den Gast wird beim absenden des Formulars gesendet.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Anmeldung bestätigt (S7)

URL: cafe/int:cafe/device/str:device_identifier/confirm/

Name: register_device_final

Die Seite Anmeldung bestätigt zeigt einen Hinweis dass die Anmeldung des Gerätes erfolgreich abgeschlossen wurde.

Die Geräte ID ist in der URL der Seite festgelegt.

#### Sicherheit

Die Seite ist ohne Zugangsbeschränkung oder Anmeldung erreichbar.

### Geräte Detailseite (S5)

URL: device/str:device_identifier/

Name: view_device

Die Geräte Detailseite zeigt die Informationen `Art des Geräts`, `Hersteller & Modell/Typ`, `Fehlerbeschreibung`, `Foto vom Gerät`, `Foto vom Typenschild` und `Folgetermin` an.

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

#### Variante: Neuer Gast (F1)

Als neuer Gast der ein defekten Geräte anmelden möchte,

- gehe ich auf die Seite (S1) der Repair-Café Termine. Dort klicke ich auf `Gerät anmelden` bei dem richtigen Repair-Café Termin. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S2) enthält ein Formular mit den Feldern `eMail-Adresse`, `Art des Geräts`, `Hersteller & Modell/Typ`, `Fehlerbeschreibung`, `Foto vom Gerät`, `Foto vom Typenschild`, ein Kontrollkästchen `Folgetermin`, ein Kontrollkästchen `Informationen zur Reparaturabwicklung` une ein Kontrollkästchen `Datenschutz`. Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S3) enthält ein Formular mit den Feldern `Name`, `Telefon` und `Wohnort`. Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`.  Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S5) bestätigt mir die Anmeldung meines Gerätes.
- In meinem eMail Posteingang finde ich ebenfalls eine Bestätigung der Geräteanmeldung.

#### Variante: Bekannter Gast (existierende eMail Adresse) (F2)

Als bekannter Gast der ein defekten Geräte anmelden möchte,

- gehe ich auf die Seite (S1) der Repair-Café Termine. Dort klicke ich auf `Gerät anmelden` bei dem richtigen Repair-Café Termin. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S2) enthält ein Formular mit den Feldern `eMail-Adresse`, `Art des Geräts`, `Hersteller & Modell/Typ`, `Fehlerbeschreibung`, `Foto vom Gerät`, `Foto vom Typenschild`, ein Kontrollkästchen `Folgetermin`, ein Kontrollkästchen `Informationen zur Reparaturabwicklung` une ein Kontrollkästchen `Datenschutz`. Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`. Dieser Klick bringt mich auf die nächste Seite.
- Die nächste Seite (S5) bestätigt mir die Anmeldung meines Gerätes.
- In meinem eMail Posteingang finde ich ebenfalls eine Bestätigung der Geräteanmeldung.

## Konfigurationsparameter

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_EMAIL_HOST
- DJANGO_EMAIL_PORT
- DJANGO_EMAIL_HOST_USER
- DJANGO_EMAIL_HOST_PASSWORD
- DJANGO_EMAIL_USE_TLS
- OIDC_RP_CLIENT_SECRET

### Feste Konfiguration

- ALLOWED_HOSTS
- LANGUAGE_CODE
- TIME_ZONE
- CSRF_TRUSTED_ORIGINS
- AUTH_USER_MODEL
- AUTHENTICATION_BACKENDS
- LOGIN_REDIRECT_URL
- OIDC_RP_CLIENT_ID
- OIDC_RP_SIGN_ALGO
- OIDC_OP_JWKS_ENDPOINT
- OIDC_OP_AUTHORIZATION_ENDPOINT
- OIDC_OP_TOKEN_ENDPOINT
- OIDC_OP_USER_ENDPOINT
- LOGIN_REDIRECT_URL
- LOGOUT_REDIRECT_URL

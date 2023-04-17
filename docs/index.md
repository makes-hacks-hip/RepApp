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

- [ ] (A1) Als Gast möchte ich einen Termin für eine Reparatur vereinbaren.
- [ ] (A2) Als Gast möchte ich eine Bestätigung für eine Reparaturanfrage bekommen.
- [ ] (A3) Als Gast möchte ich eine Terminbenachrichtigung oder eine Absage bekommen.
- [ ] (A4) Als Gast möchte ich mein angemeldetes Gerät und dessen Status einsehen können.
- [ ] (A5) Als Gast möchte ich Rückfragen zum Gerät empfangen und diese beantworten können.
- [ ] (A6) Als Gast möchte ich ein Gerät für eine Folgereparatur anmelden können

### Reparateur

- [ ] (A7) Als Reparateur möchte ich die angemeldeten Geräte ansehen können.
- [ ] (A8) Als Reparateur möchte ich mir ein angemeldetes Gerät zuordnen können.
- [ ] (A9) Als Reparateur möchte ich ein angemeldetes Gerät ablehnen können.
- [ ] (A10) Als Reparateur möchte ich Rückfragen zum Gerät stellen können.
- [ ] (A11) Als Reparateur möchte ich eine Benachrichtigung bekommen wenn eine Rückfrage beantwortet wird.
- [ ] (A12) Als Reparateur möchte ich eine Benachrichtigung bekommen wenn mir ein Gerät zugeordnet wird.
- [ ] (A13) Als Reparateur möchte ich mich für ein Repair-Café anmelden können.
- [ ] (A14) Als Reparateur möchte ich mich für ein Repair-Café abmelden können.

### Organisator

- [ ] (A15) Als Organisator möchte ich ein Repair-Café anlegen können.
- [ ] (A16) Als Organisator möchte ich die Geräte einsehen können.
- [ ] (A17) Als Organisator möchte ich eine Rückfrage zu einem Geräte stellen können.
- [ ] (A18) Als Organisator möchte ich ein Geräte ablehnen können.
- [ ] (A19) Als Organisator möchte ich ein Geräte zu einem Termin zuordnen können.
- [ ] (A20) Als Organisator möchte ich einen Reparateur zu einem Termin zuordnen können.

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

Technische Attribute:

- Identifier: SHA256 Hash aus Name + Wohnort + Timestamp

### Gerät

Ein Gerät ist ein defekter Gegenstand der im Rahmen eines Repair-Cafés repariert werden soll.

Attribute:

- Gerät: Bezeichnung des Geräts
- Fehler: Beschreibung des Defekts
- Folgetermin: Boolesches Flag das anzeigt ob es sich um einen Folgetermin handelt.

Technische Attribute:

- Identifier: SHA256 Hash aus Gerät + Gast + Timestamp
- GastId: Referenz zum Gast der das Gerät besitzt

Annahmen:

- Für einen Folgetermin werden alle Daten neu eingegeben. Eine Folgereparatur auf Basis der ersten Anmeldung kann später umgesetzt werden.

### Termin

Ein Termin ist eine Zuordnung von einem Gerät zu einem Zeitslot der Repair-Café Veranstaltung und einem Reparateur.
Ein Termin ist bestätigt, wenn eine Organisator eine Termineinladung gesendet hat und er Gast diese bestätigt hat. 

Attribute:

- Uhrzeit: Uhrzeit des Termins
- Betätigt: Boolesches Flag. True wenn eine Einladung gesendet und bestätigt wurde.

Technische Attribute:

- CafeId: Referenz zum Cafe
- ReparateurId: Referenz um Reparateur oder NULL
- GerätId: Referenz zum Gerät

### Frage

Eine Frage ist eine Rückfrage nach mehr Informationen zu einem Gerät, erstellt von einem Organisator oder einem Reparateur.

Attribute:

- Frage: Frage zum Gerät oder Defekt
- Antwort: Antwort des Gastes
- Datum: Datum der Erstellung der Rückfrage

Technische Attribute:

- OrganisatorId: Referenz zum Organisator oder NULL
- ReparateurId: Referenz zum Reparateur oder NULL
- GerätId: Referenz zum Gerät

### Kandidat

Ein Kandidat ist ein Geräte ohne festen Termin.
Diese Geräte werden von den Gästen zu Beginn des Repair-Café gebracht und am Ende abgeholt.
Falls ein Reparateur Zeit hat kann er eines dieser Geräte reparieren.

- Betätigt: Boolesches Flag. True wenn eine Einladung gesendet und bestätigt wurde.

Technische Attribute:

- CafeId: Referenz zum Cafe
- ReparateurId: Referenz um Reparateur oder NULL
- GerätId: Referenz zum Gerät

## Ansichten

### (S1) Landing Page: Repair-Cafés

Liste der Repair-Café Termine

### (S2) Gerät anmelden

Das Formular zum anmelden der Geräte hat die Felder `eMail-Adresse`, `Gerätebezeichnung`, `Fehlerbeschreibung`, eine Kontrollkästchen `Folgetermin` und einen Knopf `Absenden` zum senden des Formulars.

### (S3) Gast anmelden

Das Formular zum anmelden eines neuen Gastes hat die Felder `Name`, `Telefon`, `Wohnort` und einen Knopf `Absenden` zum senden des Formulars.

### (S4) Anmeldebestätigung

Die Anmeldebestätigung zeigt die Geräte und Gast Daten erneut an, zusammen mit der Information dass das Gerät angelegt.
Weiter enthält die Ansicht einen Link zur Geräte Detailseite und einen Link zur Gast Detailseite.

### (S5) Geräte Detailseite

Die Geräte Detailseite hat die Felder `Gerätebezeichnung`, `Fehlerbeschreibung` und eine Kontrollkästchen `Folgetermin` die mit den Angaben des Gastes ausgefüllt sind.
Weiter enthält die Seite einen Knopf `Aktualisieren` der das Formular absendet und die Daten aktualisiert und einen Link zur Detailseite des Gastes.

### (S6) Gast Detailseite

Die Gast Detailseite hat die Felder `Name`, `eMail`, `Telefon` und `Wohnort` die mit den Angaben des Gastes ausgefüllt sind.
Weiter enthält die Seite einen Knopf `Aktualisieren` der das Formular absendet.
Die Ansicht enthält auch eine Liste mit Links zu allen Geräten die der Gast angemeldet hat.

## Abläufe

### Anmeldung eines defekten Gerätes

#### Variante: Neuer Gast

Als neuer Gast der ein defekten Geräte anmelden möchte,

- gehe ich auf die Seite (S1) der Repair-Café Termine.
- dort klicke ich auf `Gerät anmelden` bei dem richtigen Repair-Café Termin.
- Der Link bringt mich auf eine neue Seite (S2) mit einem Formular.
- Das Formular hat die Felder `eMail-Adresse`, `Gerätebezeichnung` und `Fehlerbeschreibung` und eine Kontrollkästchen `Folgetermin`.
- Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`.
- Der Klick auf Absenden bringt mich zu einer neuen Seite (S3) mit einem Formular.
- Das Formular hat die Felder `Name`, `Telefon` und `Wohnort`.
- Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`.
- Der Link bringt mich auf eine neue Seite (S4) die bestätigt dass mein Gerät angemeldet wurde, die Geräte Daten und meine Daten zur Bestätigung anzeigt und einen Link zu einer `Geräte Detailseite` (S4) und einen Link zu einer `Gast Detailseite` (S6) hat.
- In meinem eMail Posteingang finde ich eine Bestätigung der Geräteanmeldung die ebenfalls den Link zur `Geräte Detailseite` und den Link zur `Gast Detailseite` enthält.

#### Variante: Existierender Gast

Als neuer Gast der ein defekten Geräte anmelden möchte,

- gehe ich auf die Seite (S1) der Repair-Café Termine.
- dort klicke ich auf `Gerät anmelden` bei dem richtigen Repair-Café Termin.
- Der Link bringt mich auf eine neue Seite (S2) mit einem Formular.
- Das Formular hat die Felder `eMail-Adresse`, `Gerätebezeichnung` und `Fehlerbeschreibung` und eine Kontrollkästchen `Folgetermin`.
- Nachdem ich die Felder ausgefüllt habe klicke auf auf `Absenden`.
- Der Link bringt mich auf eine neue Seite (S4) die bestätigt dass mein Gerät angemeldet wurde, die Geräte Daten und meine Daten zur Bestätigung anzeigt und einen Link zu einer `Geräte Detailseite` (S4) und einen Link zu einer `Gast Detailseite` (S6) hat.
- In meinem eMail Posteingang finde ich eine Bestätigung der Geräteanmeldung die ebenfalls den Link zur `Geräte Detailseite` und den Link zur `Gast Detailseite` enthält.

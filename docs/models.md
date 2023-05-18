# Daten


## Benutzer

Ein Repapp-Benutzer erweitert den Standard-Benutzer um eine eindeutige eMail-Adresse, um diese als Identifikationsmerkmal verwenden zu können.

## Cafe

Ein Cafe ist ein Repair-Café Termin.

Attribute:

- Ort: Beschreibung wo das Repair-Café stattfindet
- Adresse: Adresse an der das Repair-Café stattfindet
- Datum: Datum der Veranstaltung

Annahmen:

- Ein Repair-Café beginnt um 13:00 Uhr.
- Ein Repair-Café hat drei aufeinanderfolgende Zeitslots pro Reparateur mit je einer Stunde

## Reparateur

Ein Reparateur ist ein Mitglied des Repair-Cafés das Gäste bei der Reparatur ihrer Geräte unterstützt.

Attribute:

- Name: Name des Reparateurs
- Mail: eMail-Adresse für Benachrichtigungen

Annahmen:

- Reparateure sind immer verfügbar, d.h. Zeitslots für jeden Reparateur werden zu einem neuen Repair-Café Termin automatisch hinzugefügt.
- Reparateure können alles reparieren. Geräte Kategorien, Skills, ... werden im Moment nicht berücksichtigt. 

## Organisator

Ein Organisator ist ein Mitglied des Repair-Cafés das Reparaturtermine mit den Gästen vereinbart.

Attribute:

- Name: Name des Organisators
- Mail: eMail-Adresse für Benachrichtigungen

## Gast

Ein Gast ist ein Gerätebesitzer, der ein Gerät zur Reparatur anmeldet.

Attribute:

- Name: Name des Gastes
- Telefon: Festnetz oder Mobilnummer des Gastes
- Wohnort: Wohnort des Gastes
- Mail: eMail-Adresse des Gastes für Benachrichtigungen

Technische Attribute:

- Identifier: SHA256 Hash aus Name + Wohnort + Timestamp
- Benutzer: Referenz zum Benutzer der für diesen Gast erstellt wurde.

## Gerät

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

## Termin

Ein Termin ist eine Zuordnung von einem Gerät zu einem Zeitslot der Repair-Café Veranstaltung und einem Reparateur.
Ein Termin ist bestätigt, wenn eine Organisator eine Termineinladung gesendet hat und er Gast diese bestätigt hat. 

Attribute:

- Uhrzeit: Uhrzeit des Termins
- Betätigt: Boolesches Flag. True wenn die Einladung vom Gast bestätigt wurde.

Technische Attribute:

- Cafe: Referenz zum Cafe
- Reparateur: Referenz um Reparateur oder NULL
- Gerät: Referenz zum Gerät

## Frage

Eine Frage ist eine Rückfrage nach mehr Informationen zu einem Gerät, erstellt von einem Organisator oder einem Reparateur.

Attribute:

- Frage: Frage zum Gerät oder Defekt
- Antwort: Antwort des Gastes
- Erstellungsdatum: Datum der Erstellung der Rückfrage

Technische Attribute:

- Organisator: Referenz zum Organisator oder NULL
- Reparateur: Referenz zum Reparateur oder NULL
- Gerät: Referenz zum Gerät

## Kandidat

Ein Kandidat ist ein Geräte ohne festen Termin.
Diese Geräte werden von den Gästen zu Beginn des Repair-Café gebracht und am Ende abgeholt.
Falls ein Reparateur Zeit hat kann er eines dieser Geräte reparieren.

- Bestätigt: Boolesches Flag. True wenn die Einladung vom Gast bestätigt wurde.

Technische Attribute:

- Cafe: Referenz zum Cafe
- Gerät: Referenz zum Gerät

## Einmal-Login

Ein Einmal-Login ist ein Geheimnis das es einem Gast erlaubt sich einmalig damit anzumelden.

- Geheimnis: Geheimnis um den Gast zu identifizieren.
- URL: URL die nach der Anmeldung angezeigt werden soll.
- Erstellungsdatum: Datum an dem der Einmal-Login angelegt wurde.
- Login benutzt?: Boolesches Flag. True wenn der Einmal-Login bereits benutzt wurde.
- Login Datum: Datum an dem der Einmal-Login benutzt wurde, oder Datum der Erstellung, da das Feld aus technischen Gründen nicht leer sein kann.

Technische Attribute:

- Benutzer: Referenz zum Benutzer

## Nachricht

Eine Nachricht ist eine Anfrage von einem Gast.

- Nachricht: Anfrage des Gastes.
- Antwort: Antwort an den Gast.
- Erstellungsdatum: Datum an dem die Anfrage erstellt wurde.

Technische Attribute:

- Gast: Referenz zum Gast

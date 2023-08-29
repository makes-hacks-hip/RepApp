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

## Anmelde Konzept

RepApp unterstützt pro Benutzer-Gruppe verschiedenen Anmelde-Konzepte.

### Gäste

Für Gäste gibt es Einmal-Logins. Ein Einmal-Login ist ein Geheimnis und eine Ziel-URL, das dem Gast in From eines Anmelde-Links in einer eMail mitgeteilt wird. Mit diesem Link kann der Gast sich einmalig anmelden, da das Geheimnis danach potentiell Dritten bekannt ist, z.B. über die Browser History.

Nach dem erfolgreichen Login wird der Gast automatisch zu der hinterlegten URL weitergeleitet. Dieser Mechanismus erlaubt es einem Gast "per Klick" Zugriff auf geschützte Daten zu geben.

Wenn ein Gast versucht den Einmal-Link nochmals zu verwenden, schlägt dies Fehl, und dem Gast wird automatisch ein neuer Einmal-Link per eMail mitgeteilt. Dies wird dem Gast auch über entsprechende Nachrichten mitgeteilt.

### Mitarbeiter

Der Login für Mitarbeiter ist nur über das Single-Sign-On der Repair-Cafés erlaubt (Keycloak), das mittels OIDC angebunden ist. Alle Mitarbeiter im Repair-Café haben dort bereits einen Benutzer, was zum einen sicherstellt dass es sich um einen Mitarbeiter handelt, und zum anderen auch die Veraltung der Benutzer in RepApp vereinfacht.

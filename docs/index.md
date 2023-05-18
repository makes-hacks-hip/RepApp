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

Für Gäste wird automatsch ein Benutzerkonto angelegt, mit einem generierten, sicheren Passwort. Mit der eMail Adresse und dem Passwort kann ein Gast sich in der RepApp anmelden um seine Daten sehen und bearbeiten zu können.

### Einmal-Login

Für Gäste gibt es Einmal-Logins als Alternative. Ein Einmal-Login ist ein Geheimnis und eine Ziel-URL, das dem Gast in From eines Anmelde-Links in einer eMail mitgeteilt wird. Mit diesem Link kann der Gast sich einmalig anmelden, da das Geheimnis danach potentiell Dritten bekannt ist, z.B. über die Browser History.

Nach dem erfolgreichen Login wird der Gast automatisch zu der hinterlegten URL weitergeleitet. Dieser Mechanismus erlaubt es einem Gast "per Klick" Zugriff auf geschützte Daten zu geben.

Wenn ein Gast versucht den Einmal-Link nochmals zu verwenden, schlägt dies Fehl, und dem Gast wird automatisch ein neuer Einmal-Link per eMail mitgeteilt. Dies wird dem Gast auch über entsprechende Nachrichten mitgeteilt.

### Mitarbeiter

Der Login für Mitarbeiter ist nur über das Single-Sign-On der Repair-Cafés erlaubt (Keycloak), das mittels OIDC angebunden ist. Alle Mitarbeiter im Repair-Café haben dort bereits einen Benutzer, was zum einen sicherstellt dass es sich um einen Mitarbeiter handelt, und zum anderen auch die Veraltung der Benutzer in RepApp vereinfacht.

## Geräte

Zur Reparatur angemeldete Geräte können in den folgenden Zuständen sein:

- (0) Neu: Das Gerät wurde vom Gast angemeldet und muss als nächstes durch einen Organisator überprüft werden.
- (-1) Neu: Das Gerät wurde abgelehnt.
- (1) Rückfrage: Bei der Überprüfung durch einen Organisator wurde festgestellt dass benötigte Informationen fehlen und eine Rückfrage an den Gast gesendet. Die Antwort ist noch nicht eingetroffen.
- (2) Rückfrage beantwortet: Eine Rückfrage der Organisation wurde durch den Gast beantwortet. Als nächstes muss die Antwort durch einen Organisator überprüft werden.
- (3) Warteliste: Das Gerät wurde durch die Organisation überprüft und kann einem Repair-Café zugeordnet werden. Jetzt können Reparateure das Gerät einsehen.
- (4) Reserviert: Ein Reparateur hat sich das Gerät zugeordnet.
- (6) Zugeordnet: Das Gerät ist einem Repair-Café zugeordnet.
- (7) Gebucht: Das Gerät ist einem Reparaturtermin zugeordnet.

## Konfigurationsparameter

- DJANGO_SECRET_KEY: Secret Key für das Django Framework.
- DJANGO_DEBUG: Debug-Modus verwenden? Standard ist True.

- DJANGO_EMAIL_HOST: eMail Server
- DJANGO_EMAIL_PORT: eMail Server Port
- DJANGO_EMAIL_HOST_USER: Benutzername für den eMail Server
- DJANGO_EMAIL_HOST_PASSWORD: Passwort für den eMail Server
- DJANGO_EMAIL_USE_TLS: TLS verwenden? Standard ist True.

- OIDC_RP_CLIENT_SECRET: Secret für den OIDC Prozess. Ist auch im Keycloak konfiguriert.

### Feste Konfiguration

- ALLOWED_HOSTS: Erlaubte Domainnamen. ("127.0.0.1", "localhost", "repapp.rc-hip.de", "anmeldung.repaircafe-hilpoltstein.de")
- LANGUAGE_CODE: de
- TIME_ZONE: Europe/Berlin
- CSRF_TRUSTED_ORIGINS: Siehe ALLOWED_HOSTS.
- AUTH_USER_MODEL: CustomUser in RepApp Models definiert.
- AUTHENTICATION_BACKENDS: Standard + Backends aus RepApp Backends.

- OIDC_RP_CLIENT_ID: OIDC Client ID, im Keycloak konfiguriert.
- OIDC_RP_SIGN_ALGO: RS256
- OIDC_OP_JWKS_ENDPOINT: Keycloak URL
- OIDC_OP_AUTHORIZATION_ENDPOINT: Keycloak URL
- OIDC_OP_TOKEN_ENDPOINT: Keycloak URL
- OIDC_OP_USER_ENDPOINT: Keycloak URL

- LOGIN_REDIRECT_URL: Debug: 127.0.0.1:8000, sonst https://anmeldung.repaircafe-hilpoltstein.de/
- LOGOUT_REDIRECT_URL: Siehe LOGIN_REDIRECT_URL

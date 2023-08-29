# Repapp configuration

## Debug mode

The Django debug mode is activated if there is a environment variable `DJANGO_DEBUG` with the value "true", "1" or "t". By default, the debug mode is disabled. 

## Organization name

Some templates use and organization name. This value is taken from `settings.ORGANIZATION` and defaults to "Repair-Café Hilpoltstein".

## Email settings

The following environment variables are used to configure the Django email feature:

``` Python
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", "")
EMAIL_PORT = (int)(os.getenv("DJANGO_EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", None)
EMAIL_USE_TLS = os.getenv("DJANGO_EMAIL_USE_TLS", "true") in ("true", "1", "t")
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_SENDER_ADDRESS", "")
```
See https://docs.djangoproject.com/en/4.2/topics/email/ for more details.

## Translations

Repapp is using localization, and comes with german and english translations.

Enable the `LocaleMiddleware`:

```Python
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    # enable translation
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
```

We use the following localization settings:

```Python
LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

Also the URLs are localized, and the language is choosen using i18n URL patterns:

```Python
...
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('one_time_login/'),
         include('one_time_login.urls', namespace='one_time_login')),
    # URLs for rosetta translation interface
    path('rosetta/', include('rosetta.urls')),
)
```

### Rosetta

For translating the interface, we use rosetta. For more details see https://pypi.org/project/django-rosetta/.

You need to install rosetta (`pip install django-rosetta`) and enable it in the apps:

```Python
INSTALLED_APPS = [
    ...
    # enable rosetta online translation interface
    'rosetta',
    ...
]
```

Rosatta is made availabel at `rosetta/`.

## One time login

To enable the one time login links, an additional authentication backend must get added:

```Python
# Repapp specific authentication backends
AUTHENTICATION_BACKENDS = [
    # Backend for one time logins
    "one_time_login.authentication_backends.OneTimeLoginBackend",
]
```

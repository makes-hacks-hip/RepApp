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
```
See https://docs.djangoproject.com/en/4.2/topics/email/ for more details.


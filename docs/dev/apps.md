# Apps

The repapp is split into different modules, realized as Django apps, to improve the maintainability.

## One time login

The one time login module provides a login for guests using a one time secret as part of an URL.

### Settings

- The templates use the `settings.ORGANIZATION` variable to fill the organization name.
- The Django mail module is used to send emails. See https://docs.djangoproject.com/en/4.2/topics/email/ for details how to configure the mail host.

### Configuration

To enable the one time login links, an additional authentication backend must get added:

```Python
# Repapp specific authentication backends
AUTHENTICATION_BACKENDS = [
    # Backend for one time logins
    "one_time_login.authentication_backends.OneTimeLoginBackend",
]
```
The one time login urls must get added using namespace `one_time_login`:


```Python
urlpatterns = i18n_patterns(
    ...
    path(_('one_time_login/'),
         include('one_time_login.urls', namespace='one_time_login')),
    ...
)
```

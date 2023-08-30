# Apps

The repapp is split into different modules, realized as Django apps, to improve the maintainability.

## One time login

The one time login module provides a login for guests using a one time secret as part of an URL.

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

## Email interface

The email interface modules supports handling of mails. It support sending of mails, including HTML formatting and attachments, and it supports receiving of plain text and HTML formatted mails, including attachments.

- The Django mail module is used to send emails. See https://docs.djangoproject.com/en/4.2/topics/email/ for details how to configure the mail host.
- CKEditor is used for email content editing. See https://django-ckeditor.readthedocs.io/en/latest/ for details.
- Crispy forms is used for form rendering. See https://django-crispy-forms.readthedocs.io/en/latest/ for details.
- Bootstrap 5 theme for crispy forms is used. See https://github.com/django-crispy-forms/crispy-bootstrap5 for details.

### Configuration

The email interface urls must get added using namespace `email_interface`:

```Python
urlpatterns = i18n_patterns(
    ...
    path(_('emails/'),
         include('email_interface.urls', namespace='email_interface')),
    ...
)
```

To use CKEditor as authenticated user, the following additional urls must get added:

```Python
urlpatterns = i18n_patterns(
    ...
    # CKEditor upload views
    path('upload/', login_required(ckeditor_views.upload), name="ckeditor_upload"),
    path('browse/', never_cache(login_required(ckeditor_views.browse)),
         name="ckeditor_browse"),
    ...
)
```

To be abel to use CKEditor also the static an media content must get served. For development this is done with:

```Python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
```

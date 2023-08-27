# Apps

The repapp is split into different modules, realized as Django apps, to improve the maintainability.

## one time login

The one time login module provides a login for guests using a one time secret as part of an URL.

### Settings

- The templates use the `settings.ORGANIZATION` variable to fill the organization name.
- The Django mail module is used to send emails. See https://docs.djangoproject.com/en/4.2/topics/email/ for details how to configure the mail host.

## mail interface


## repapp members

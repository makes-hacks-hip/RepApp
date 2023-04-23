"""
Django settings for rc_hip project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import mimetypes
import os
from pathlib import Path

mimetypes.add_type("text/css", ".css", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-ura&_-(r(&&b$0s!a=07c@k6c!8=8m7$5(4#w8m@79-e%rn6s*'
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", 'django-insecure-ura&_-(r(&&b$0s!a=07c@k6c!8=8m7$5(4#w8m@79-e%rn6s*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", 'true').lower() in ('true', '1', 't')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'repapp.rc-hip.de'
]

# Application definition

INSTALLED_APPS = [
    'repapp.apps.RepappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'repapp_users.apps.RepappUsersConfig',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rc_hip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rc_hip.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_TRUSTED_ORIGINS = [
    'https://repapp.rc-hip.de',
    'http://127.0.0.1:8020'
]

EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", '')
EMAIL_PORT = (int)(os.getenv("DJANGO_EMAIL_PORT", '25'))
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", None)
EMAIL_USE_TLS = os.getenv("DJANGO_EMAIL_USE_TLS", 'true') in ('true', '1', 't')

AUTH_USER_MODEL = "repapp_users.CustomUser"
AUTHENTICATION_BACKENDS = [
    "repapp_users.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    # 'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'repapp_users.backends.KeycloakOIDCAB'
]

LOGIN_REDIRECT_URL = '/guest/profile/'

OIDC_RP_CLIENT_ID = "repapp"
OIDC_RP_CLIENT_SECRET = os.getenv("DJANGO_OIDC_RP_CLIENT_SECRET", None)

OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_JWKS_ENDPOINT = "https://sso.makes-hacks-hip.de/realms/Makes-Hacks-Hip/protocol/openid-connect/certs"

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://sso.makes-hacks-hip.de/realms/Makes-Hacks-Hip/protocol/openid-connect/auth"
OIDC_OP_TOKEN_ENDPOINT = "https://sso.makes-hacks-hip.de/realms/Makes-Hacks-Hip/protocol/openid-connect/token"
OIDC_OP_USER_ENDPOINT = "https://sso.makes-hacks-hip.de/realms/Makes-Hacks-Hip/protocol/openid-connect/userinfo"

if DEBUG:
    LOGIN_REDIRECT_URL = "http://127.0.0.1:8000/"
    LOGOUT_REDIRECT_URL = "http://127.0.0.1:8000/"
else:
    LOGIN_REDIRECT_URL = "https://repapp.rc-hip.de/"
    LOGOUT_REDIRECT_URL = "https://repapp.rc-hip.de/"

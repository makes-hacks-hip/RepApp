#!/usr/bin/env bash
cd /opt/app/rc_hip

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi

chown -R www-data:www-data /opt/app

(gunicorn rc_hip.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) & nginx -g "daemon off;"

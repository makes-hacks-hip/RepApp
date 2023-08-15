# Repapp - developer documentation

The Repapp is a repair assignment booking and management tool. 
It tries to support all common workflows happening while organizing a repair café event.
It's build using the Django web framework.

The code of the Repapp is hosted on Github: https://github.com/makes-hacks-hip/RepApp

## Local development setup

- Clone the Github repository
- Create a Python environment: `python -m venv venv`
- Activate the Python environment: `source venv/bin/activate`
- Change to the Django project folder: `cd rc_hip`
- Setup the database:
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- Setup an admin user: `python manage.py createsuperuser`
- Run the local test server: `python manage.py runserver`

## Docker image

- Build the image: `docker build -t repapp .`
- Run the image:

```bash
docker run --rm -d \
  -p 127.0.0.1:8020:8020 \
  --name repapp \
  --env DJANGO_SUPERUSER_USERNAME=suba \
  --env DJANGO_SUPERUSER_PASSWORD=ThePassword \
  --env DJANGO_SUPERUSER_EMAIL=noreply@example.com \
  repapp`
```

- Open http://127.0.0.1:8020/ in your browser

## Tests

- Unit tests: `python manage.py test`
- LiveServer tests: `python manage.py test repapp.live_tests.WorkflowTests`

# RepApp

Web App um Reparaturtermine zu vereinbaren.

For documentation see https://makes-hacks-hip.github.io/RepApp/.

## Setup for development

- Clone repo
- `python -m venv venv`
- `source venv/bin/activate`
- `cd rc_hip`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`

## Build Docker image

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
- Open `http://127.0.0.1:8020/` in your browser

## Run tests

### Unit tests

Run `python manage.py test`

### LiveServer Tests

Run `python manage.py test repapp.live_tests.WorkflowTests`

### Coverage

- `coverage run --source='.' manage.py test`
- `coverage report` or `coverage html`
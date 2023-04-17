# RepApp

Web App um Reparaturtermine zu vereinbaren.

For documentation see https://makes-hacks-hip.github.io/RepApp/.

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

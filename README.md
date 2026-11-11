# Djirection — Django Band Website
IBM Back-end Application Development Capstone by Dias Nygman. Based on the IBM Skills Network starter. AI assistance was used for coding and tests.

## Implemented
Concert, Photo and Song models; database migrations; signup/login/logout; songs with lyrics modal; photos; concert list and authenticated attendance updates; registered Concert admin.

## Configuration
`SONGS_SERVICE_URL` and `PICTURES_SERVICE_URL` point to the two REST services. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false` and appropriate `DJANGO_ALLOWED_HOSTS` for a production deployment. No default administrator or password is created. Use `python manage.py createsuperuser` interactively if needed.

## Run
`pip install -r requirements.txt`
`python manage.py migrate`
`python manage.py collectstatic --noinput`
`python manage.py runserver 0.0.0.0:8000`

Alternatively build the Dockerfile and publish port 8000. The entrypoint applies migrations. SQLite is intended for this demonstration; persist /app/db.sqlite3 or configure an external database for durable hosting.

## Validation
`python manage.py test concert -v 2`
Seven tests cover pages, authentication, attendance and service response rendering. They passed locally; live Docker services also returned HTTP 200 for home, songs and photos.
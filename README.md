# recipe-app

# run all commands through Docker Compose

docker-compose run --rm app sh -c "python manage.py collectstatic

# create file requirements.txt, add :

Django==5.2.6
django-cors-headers==4.7.0
django-crispy-forms==2.4
django-redis==6.0.0
django-rest-framework==0.1.0
django_celery_results==2.6.0
djangorestframework==3.16.1`
djangorestframework_simplejwt==5.5.1

# create docker file

Dockerfile

# run dockerfile

docker build .

# run docker compose

docker-compose build

# create file requirements.dev.txt, add :

flake8

# run flake on docker

docker-compose run --rm app sh -c "/py/bin/flake8"

# run django on docker

docker-compose run --rm app sh -c "django-admin startproject app ."

# run container

docker-compose up

# create folder .github/workflows on the root project and create checks.yml add :

---

name: Checks
on: [push]
jobs:
test-lint
name: Test and lint
runs-on: ubuntu-20.04

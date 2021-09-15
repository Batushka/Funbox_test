#!/bin/bash
set -e
# pipenv run python manage.py migrate --noinput
pipenv run python manage.py runserver 127.0.0.1:8000

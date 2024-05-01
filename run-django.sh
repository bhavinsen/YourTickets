#!/usr/bin/env bash



cd /app
source prestart.sh


python manage.py runserver 0.0.0.0:8000
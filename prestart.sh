#!/usr/bin/env bash

echo "Running prestart.sh..."

python manage.py migrate
python manage.py collectstatic --noinput

echo "Finished prestart.sh..."
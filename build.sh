#!/usr/bin/env bash
set -o errexit
pip3 install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata backup.json
#!/bin/bash

# python3 manage.py runserver 0.0.0.0:8080
python3 -m gunicorn --workers=5 olymp.wsgi:application -b 0.0.0.0:8080
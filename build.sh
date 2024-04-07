#!/bin/bash

#Build the Project

echo "Building the project ..."
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install django

echo "Make migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect static..."
python3.9 manage.py collectstatic --noinput --clear
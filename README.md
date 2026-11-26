# django-orders-practice

Small Django practice project (fake data only): an Order model with admin, plus list, add, edit and delete pages, and tests.

## Run

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Then open /orders/ or /admin/.

## Test

    python manage.py test

## Stack

Django, SQLite (PostgreSQL planned).

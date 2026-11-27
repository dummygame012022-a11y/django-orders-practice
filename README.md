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

Django, PostgreSQL (SQLite fallback).

## Config (.env)

Himoa ang `.env` file sa root sa project (dili kini i-commit). Pananglitan, placeholder ra:

    DEBUG=True
    SECRET_KEY=ibutang-dinhi-ang-imong-kaugalingong-key
    DB_NAME=orders_practice
    DB_USER=imong-db-user

- Kung walay `DB_NAME`, SQLite ang gamiton.
- Kung walay `DEBUG=True`, `False` ang default.


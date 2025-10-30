@echo off
echo ======================================
echo Event Management System - Quick Start
echo ======================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Creating database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo Step 3: Would you like to create a superuser? (Press Ctrl+C to skip)
python manage.py createsuperuser
echo.

echo Setup complete!
echo.
echo To start the server, run:
echo python manage.py runserver
echo.
pause

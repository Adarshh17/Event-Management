@echo off
echo Creating and applying database migrations...
echo.

cd /d D:\new\event_management

echo Step 1: Creating migrations...
python manage.py makemigrations

echo.
echo Step 2: Applying migrations...
python manage.py migrate

echo.
echo Done! Database tables created.
echo.
pause

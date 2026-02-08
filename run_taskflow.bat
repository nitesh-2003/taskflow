@echo off
echo.
echo ========================================
echo       TaskFlow Project Setup
echo ========================================
echo.

echo 1. Creating Virtual Environment...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate

echo 2. Installing Dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Dependency installation failed. Please check your internet connection or Python version.
    pause
    exit /b %ERRORLEVEL%
)

echo 3. Running Migrations...
python manage.py makemigrations accounts projects tasks notifications
python manage.py migrate

echo 4. Creating Superuser (Admin)...
echo Please follow prompts to create an admin user:
python manage.py createsuperuser

echo 5. Starting Development Server...
echo Server will be available at http://127.0.0.1:8000
python manage.py runserver

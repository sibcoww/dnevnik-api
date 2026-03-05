@echo off
REM Initialize Django Project Script for Windows
REM This script sets up the project with all necessary configurations

setlocal enabledelayedexpansion

echo.
echo ============================================
echo  Dnevnik API Project Initialization
echo ============================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo ^[*^] Creating .env file from .env.example...
    copy .env.example .env
    echo ^[OK^] .env created. Please update it with your configuration.
) else (
    echo ^[OK^] .env file already exists.
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo ^[*^] Creating virtual environment...
    python -m venv venv
    echo ^[OK^] Virtual environment created.
) else (
    echo ^[OK^] Virtual environment already exists.
)

REM Activate virtual environment
echo ^[*^] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo ^[*^] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ^[OK^] Dependencies installed.

REM Create logs directory
if not exist "logs" (
    mkdir logs
)

REM Run migrations
echo ^[*^] Running database migrations...
python manage.py migrate
echo ^[OK^] Migrations completed.

REM Create superuser
echo ^[*^] Creating superuser...
python manage.py createsuperuser

REM Collect static files
echo ^[*^] Collecting static files...
python manage.py collectstatic --noinput
echo ^[OK^] Static files collected.

REM Create test data (optional)
setlocal
set /p TESTDATA="Do you want to create test data? (y/n): "
if /i "%TESTDATA%"=="y" (
    echo ^[*^] Creating test data...
    python manage.py shell < create_test_data.py
    echo ^[OK^] Test data created.
)
endlocal

echo.
echo ============================================
echo  Project initialization complete!
echo ============================================
echo.
echo Next steps:
echo 1. Run: python manage.py runserver
echo 2. Admin: http://localhost:8000/admin/
echo 3. API Docs: http://localhost:8000/api/docs/
echo.

pause

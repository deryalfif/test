@echo off
echo === Student Attendance System Setup ===
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.10 or higher.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create directories
echo Creating directories...
if not exist "flask_session" mkdir flask_session
if not exist "backups" mkdir backups
if not exist "instance" mkdir instance

REM Copy .env file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

REM Initialize database
echo Initializing database...
flask init-db

REM Create admin user
echo Creating admin user...
flask create-admin

echo.
echo === Setup Complete! ===
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run the app: flask run
echo 3. Open browser: http://localhost:5000
echo.
echo Default login:
echo Username: admin
echo Password: admin123
echo.
pause

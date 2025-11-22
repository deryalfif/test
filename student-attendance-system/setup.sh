#!/bin/bash

echo "=== Student Attendance System Setup ==="
echo ""

# Check Python version
python3 --version || { echo "Python 3 not found!"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p flask_session
mkdir -p backups
mkdir -p instance

# Copy .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
fi

# Initialize database
echo "Initializing database..."
flask init-db

# Create admin user
echo "Creating admin user..."
flask create-admin

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: flask run"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "Default login:"
echo "Username: admin"
echo "Password: admin123"
echo ""

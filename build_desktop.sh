#!/bin/bash
# Build script for PreCostCalc Desktop Application
# This script builds the PyQt6 desktop application and packages it with PyInstaller

set -e

echo "=== PreCostCalc Desktop Build Script ==="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install Django==5.2.4
pip install djangorestframework==3.15.2
pip install PyQt6==6.6.1
pip install PyInstaller==6.3.0

# Ensure database is ready
echo "Setting up database..."
python manage.py migrate --run-syncdb || true

# Run the application to test
echo "Testing application..."
python desktop_app/main.py &
APP_PID=$!
sleep 3
kill $APP_PID 2>/dev/null || true

# Build with PyInstaller
echo "Building executable with PyInstaller..."
pyinstaller precostcalc_desktop.spec --clean --noconfirm

echo ""
echo "=== Build Complete ==="
echo "Executable location: dist/PreCostCalcDesktop.exe"
echo ""
echo "You can run the application with: ./dist/PreCostCalcDesktop.exe"

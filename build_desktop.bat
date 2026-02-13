@echo off
REM Build script for PreCostCalc Desktop Application (Windows)
REM This script builds the PyQt6 desktop application and packages it with PyInstaller

echo === PreCostCalc Desktop Build Script ===

REM Create virtual environment if not exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install Django==5.2.4
pip install djangorestframework==3.15.2
pip install PyQt6==6.6.1
pip install PyInstaller==6.3.0

REM Ensure database is ready
echo Setting up database...
python manage.py migrate --run-syncdb

REM Build with PyInstaller
echo Building executable with PyInstaller...
pyinstaller precostcalc_desktop.spec --clean --noconfirm

echo.
echo === Build Complete ===
echo Executable location: dist\PreCostCalcDesktop.exe
echo.
echo You can run the application with: dist\PreCostCalcDesktop.exe

pause

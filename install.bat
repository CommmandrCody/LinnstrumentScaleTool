@echo off
REM Linnstrument Scale Tool - One-line installer for Windows

echo ===========================================
echo Linnstrument Scale Tool - Installer
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Found %PYTHON_VERSION%
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --user mido python-rtmidi

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.
echo ===========================================
echo Installation complete!
echo ===========================================
echo.
echo Try it now:
echo   python scale_tool.py C major
echo.
echo For more options:
echo   python scale_tool.py --help
echo   python setup.py  (for guided setup)
echo.
echo See START_HERE.md for full getting started guide
echo.
pause

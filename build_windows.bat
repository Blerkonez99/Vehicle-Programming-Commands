@echo off
setlocal enabledelayedexpansion

REM Change to the repository root (the folder that contains this script)
cd /d "%~dp0"

REM Ensure Python is available
python --version >NUL 2>&1
if errorlevel 1 (
    echo Python is not available on PATH. Install Python 3.8+ first.
    exit /b 1
)

REM Create virtual environment if it does not exist
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip and install requirements
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM Build the GUI executable with bundled resources
pyinstaller --noconfirm --clean --name KeyProgrammer --noconsole ^
    --add-data "src\database;src\database" ^
    --add-data "config.json;." ^
    src\main.py

if errorlevel 1 (
    echo Build failed. See errors above.
    exit /b 1
)

echo Build complete! The executable is located at dist\KeyProgrammer\KeyProgrammer.exe
exit /b 0

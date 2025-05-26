@echo off

set VENV_DIR=.venv_windows

REM Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
) else (
    echo Virtual environment already exists.
)

REM Install dependencies
echo Activating virtual environment and installing packages...

call "%VENV_DIR%\Scripts\activate.bat"

python -m pip install --upgrade pip

if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Please create one using: pip freeze > requirements.txt
    exit /b 1
)

echo.
echo Setup complete.
echo To activate the virtual environment, run:
echo     call %VENV_DIR%\Scripts\activate.bat
pause

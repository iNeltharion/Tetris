@echo off

:: Check if the .venv folder exists
if not exist ".venv" (
    echo Creating a virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
echo Activating the virtual environment...
call .venv\Scripts\activate

:: Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

:: Run the application
echo Running the application...
cd game
python Tetris.py

:: Keep the console window open
pause

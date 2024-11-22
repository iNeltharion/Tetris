@echo off

:: Set required Python version
set REQUIRED_PYTHON_VERSION=3.10

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python %REQUIRED_PYTHON_VERSION%...
    goto InstallPython
)

:: Get installed Python version
for /f "tokens=2 delims= " %%v in ('python --version') do (
    for /f "tokens=1-2 delims=. " %%a in ("%%v") do (
        set INSTALLED_MAJOR=%%a
        set INSTALLED_MINOR=%%b
    )
)

:: Compare Python version
if %INSTALLED_MAJOR% lss 3 (
    echo Python version is below 3.10. Installing Python %REQUIRED_PYTHON_VERSION%...
    goto InstallPython
)

if %INSTALLED_MAJOR%==3 if %INSTALLED_MINOR% lss 10 (
    echo Python version is below 3.10. Installing Python %REQUIRED_PYTHON_VERSION%...
    goto InstallPython
)

echo Python 3.10+ is already installed.
goto SetupEnvironment

:InstallPython
:: Download Python installer
echo Downloading Python installer...
powershell -Command "& { (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/%REQUIRED_PYTHON_VERSION%/python-%REQUIRED_PYTHON_VERSION%-amd64.exe', 'python-installer.exe') }"

:: Install Python silently
echo Installing Python %REQUIRED_PYTHON_VERSION%...
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
if %errorlevel% neq 0 (
    echo Python installation failed. Please install Python manually.
    pause
    exit /b
)

:: Clean up
del python-installer.exe
echo Python installed successfully.

:SetupEnvironment
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

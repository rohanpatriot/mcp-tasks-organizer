@echo off
REM Installation script for MCP Tasks Organizer

REM Check for Python 3.10+
for /f "tokens=*" %%a in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set python_version=%%a
set required_version=3.10

REM Compare versions (crude but works for this purpose)
if %python_version% LSS %required_version% (
    echo Error: Python %required_version% or higher is required. Found Python %python_version%
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install package in development mode
echo Installing MCP Tasks Organizer...
pip install -e .

echo Installation complete! MCP Tasks Organizer is ready to use.
echo.
echo To use with Claude for Desktop, edit your claude_desktop_config.json file.
echo See the README.md for details. 
@echo off
echo ========================================
echo Medieval D&D Chatbot - Quick Setup
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    echo Make sure Python is installed and in your PATH
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Edit backend\.env if you want to add an OpenAI API key.
) else (
    echo .env file already exists, skipping...
)

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the game, run:
echo   start.bat
echo.
echo Or manually:
echo   1. cd backend
echo   2. python main.py
echo   3. Open frontend\index.html in browser
echo.
pause
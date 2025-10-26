@echo off
title Medieval D&D Chatbot - Starting...
color 0A

echo.
echo ========================================
echo    MEDIEVAL D&D CHATBOT
echo    One-Click Startup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [!] Virtual environment not found!
    echo [!] Please run setup.bat first
    echo.
    pause
    exit /b 1
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Starting backend server...
start "D&D Backend Server" cmd /k "cd backend && python main.py"

timeout /t 3 /nobreak >nul

echo [*] Starting frontend server...
start "D&D Frontend Server" cmd /k "cd frontend && python -m http.server 8080"

timeout /t 2 /nobreak >nul

echo [*] Opening game in browser...
timeout /t 2 /nobreak >nul
start http://localhost:8080

echo.
echo ========================================
echo    Game is now running!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo The game should open in your browser automatically.
echo.
echo To stop the servers:
echo   - Close both server windows, OR
echo   - Run stop.bat
echo.
echo Press any key to close this window...
pause >nul
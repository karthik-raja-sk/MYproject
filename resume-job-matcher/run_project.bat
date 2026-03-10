@echo off
TITLE AI Resume-Job Matcher - Master Controller
setlocal enabledelayedexpansion

echo ===================================================
echo 🚀 AI Resume-Job Matcher - Startup
echo ===================================================

:: 1. Database Check
echo [1/3] Checking PostgreSQL service...
net start postgresql-x64-16 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    net start postgresql >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo [!] PostgreSQL service not found or failing to start.
        echo [!] Please ensure PostgreSQL is installed and service name is correct.
    ) else (
        echo [+] PostgreSQL started successfully.
    )
) else (
    echo [+] PostgreSQL started.
)

:: 2. Start Backend
echo.
echo [2/3] Starting Backend Server...
if not exist backend\venv (
    echo [!] Backend virtual environment missing. Please run setup_project.bat first.
    pause
    exit /b
)

:: Launch Backend in separate window
start "Backend - FastAPI" cmd /k "title Backend - FastAPI && cd backend && call venv\Scripts\activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

:: 3. Start Frontend
echo.
echo [3/3] Starting Frontend Server...
if not exist frontend\node_modules (
    echo [!] Frontend dependencies missing. Please run setup_project.bat first.
    pause
    exit /b
)

:: Launch Frontend in separate window
start "Frontend - Vite" cmd /k "title Frontend - Vite && cd frontend && npm run dev"

:: 4. Final Summary
echo.
echo ===================================================
echo ✅ Application is running!
echo ===================================================
echo.
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo Frontend:  http://localhost:5173
echo.
echo 💡 Use 'stop_project.bat' (if available) or close the windows to stop.
echo 💡 troubleshooting_guide.md is available for common issues.
echo ===================================================
pause

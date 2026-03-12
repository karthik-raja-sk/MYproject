@echo off
setlocal enabledelayedexpansion

:: ==========================================
:: AI Resume-Job Matcher - Automation Script
:: ==========================================

echo [1/4] Checking System Requirements...

:: --- Python Detection ---
set "PYTHON_CMD="
python --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PYTHON_CMD=python"
) else (
    python3 --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set "PYTHON_CMD=python3"
    ) else (
        py --version >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            set "PYTHON_CMD=py"
        )
    )
)

if not defined PYTHON_CMD (
    echo [ERROR] Python not found! Please install Python and add it to your PATH.
    pause
    exit /b 1
)
echo [INFO] Using Python: !PYTHON_CMD!

:: --- npm Detection ---
set "NPM_CMD="
npm --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "NPM_CMD=npm"
)

if not defined NPM_CMD (
    echo [ERROR] Node.js/npm not found! Please install Node.js and add it to your PATH.
    pause
    exit /b 1
)
echo [INFO] Using npm: !NPM_CMD!

:: --- Setup Backend ---
echo [2/4] Setting up Backend...
pushd "%~dp0backend"
if not exist venv (
    echo [INFO] Creating virtual environment...
    "!PYTHON_CMD!" -m venv venv
)
echo [INFO] Installing backend dependencies...
call venv\Scripts\activate
"!PYTHON_CMD!" -m pip install --upgrade pip
"!PYTHON_CMD!" -m pip install -r requirements.txt
popd

:: --- Setup Frontend ---
echo [3/4] Setting up Frontend...
pushd "%~dp0frontend"
if not exist node_modules (
    echo [INFO] Installing frontend dependencies...
    call "!NPM_CMD!" install
)
popd

:: --- Start Project ---
echo [4/4] Starting Project...

:: Start Backend in a new window
echo [INFO] Starting Backend Server...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

:: Start Frontend in a new window
echo [INFO] Starting Frontend Server...
start "Frontend - Vite" cmd /k "cd /d %~dp0frontend && npm run dev"

:: Wait for servers to initialize
echo [INFO] Waiting for servers to start...
timeout /t 5 /nobreak >nul

:: Open Browser
echo [INFO] Opening Browser...
start "" "http://localhost:5173"

echo.
echo =========================================
echo PROJECT IS RUNNING!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo =========================================
echo.
pause

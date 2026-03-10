@echo off
TITLE AI Resume-Job Matcher - Setup Wizard
setlocal enabledelayedexpansion

echo ===================================================
echo 🛠️ AI Resume-Job Matcher - Initial Setup
echo ===================================================

:: 1. Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org
    pause
    exit /b
)
echo [+] Python detected.

:: 2. Check for Node.js
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Node.js is not installed or not in PATH.
    echo Please install Node.js 18+ from nodejs.org
    pause
    exit /b
)
echo [+] Node.js detected.

:: 3. Setup Backend
echo.
echo [1/3] Setting up Backend...
cd backend
if not exist venv (
    echo [+] Creating virtual environment...
    python -m venv venv
)
echo [+] Activating virtual environment...
call venv\Scripts\activate
echo [+] Installing Backend dependencies (this may take a few minutes)...
pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [!] Failed to install backend dependencies.
    pause
    exit /b
)
cd ..

:: 4. Setup Frontend
echo.
echo [2/3] Setting up Frontend...
cd frontend
echo [+] Installing Frontend dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [!] Failed to install frontend dependencies.
    pause
    exit /b
)
cd ..

:: 5. Database Reminder
echo.
echo [3/3] Finalizing...
if not exist .env (
    echo [+] Creating .env from .env.example (if it exists)...
    if exist backend\.env.example (
        copy backend\.env.example .env
    ) else (
        echo DATABASE_URL=postgresql://postgres:password@localhost:5432/resume_matcher > .env
        echo JWT_SECRET=change_me_secret_key >> .env
        echo MODEL_NAME=all-MiniLM-L6-v2 >> .env
        echo API_BASE_URL=http://localhost:8000 >> .env
    )
)

echo ===================================================
echo ✅ Setup Complete!
echo ===================================================
echo.
echo 🚨 IMPORTANT: 
echo 1. Ensure PostgreSQL is running.
echo 2. Create the database manually: 'createdb -U postgres resume_matcher'
echo 3. Update the password in '.env' if necessary.
echo.
echo Now you can run the project using: run_project.bat
echo ===================================================
pause

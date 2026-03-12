# ==============================================================================
# Resume-Job Matcher - Automation Script (Windows PowerShell)
# Senior Architect & DevOps Engineer Edition
# ==============================================================================

# Script Configuration
$ProjectRoot = Get-Location
$BackendPath = Join-Path $ProjectRoot "backend"
$FrontendPath = Join-Path $ProjectRoot "frontend"
$VenvName = ".venv"
$VenvPath = Join-Path $BackendPath $VenvName

Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   AI Resume-Job Matcher - Startup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Prerequisites Check
Write-Host "`n[1/5] Checking System Prerequisites..." -ForegroundColor Yellow

# Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python not found in PATH. Please install Python." -ForegroundColor Red
    exit 1
}
$PythonVersion = python --version
Write-Host "[INFO] Detected Python: $PythonVersion"

# Check Node.js
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] npm (Node.js) not found in PATH. Please install Node.js." -ForegroundColor Red
    exit 1
}
Write-Host "[INFO] Detected npm: $(npm -v)"

# 2. Database Readiness & Auto-Creation
Write-Host "`n[2/5] Ensuring Database is Ready..." -ForegroundColor Yellow
$Port = 5432

if (!(Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet)) {
    Write-Host "[ERROR] PostgreSQL is not running on port $Port. Please start PostgreSQL." -ForegroundColor Red
    exit 1
}

# Run a robust python script to ensure the DB and tables exist
Write-Host "[INFO] Verifying/Creating database and tables..." -ForegroundColor Gray
python init_project_db.py

Write-Host "[INFO] Database is ready." -ForegroundColor Green

# 3. Backend Setup
Write-Host "`n[3/5] Setting up Backend Environment..." -ForegroundColor Yellow
Set-Location $BackendPath

# Create Virtual Environment if it doesn't exist
if (!(Test-Path $VenvName)) {
    Write-Host "[INFO] Creating virtual environment in $VenvName..." -ForegroundColor Gray
    python -m venv $VenvName
}

# Source the activation script for the current process
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
& $ActivateScript

# Install/Update Backend Dependencies
Write-Host "[INFO] Updating pip and installing dependencies..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
python -m pip install bcrypt==3.2.0 --quiet

# 4. Frontend Setup
Write-Host "`n[4/5] Setting up Frontend Dependencies..." -ForegroundColor Yellow
Set-Location $FrontendPath

if (!(Test-Path "node_modules")) {
    Write-Host "[INFO] node_modules not found. Installing frontend dependencies (this may take a minute)..." -ForegroundColor Gray
    npm install --silent
}
else {
    Write-Host "[INFO] Frontend dependencies already installed." -ForegroundColor Green
}

# 5. Launching Servers
Write-Host "`n[5/5] Launching Servers..." -ForegroundColor Yellow
Set-Location $ProjectRoot

# Launch Backend in a new window
Write-Host "[LAUNCH] Starting FastAPI Backend on 0.0.0.0:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; & .\$VenvName\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

# Launch Frontend in a new window
Write-Host "[LAUNCH] Starting Vite Frontend on localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowStyle Normal

# Wait for services to warm up
Write-Host "`nWaiting for servers to initialize (8s)..." -ForegroundColor Gray
Start-Sleep -Seconds 8

# Open browser
Write-Host "[INFO] Launching browser: http://localhost:5173" -ForegroundColor Cyan
Start-Process "http://localhost:5173"

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "   SYSTEM IS RUNNING SUCCESSFULLY" -ForegroundColor Green
Write-Host "   Backend: http://127.0.0.1:8000"
Write-Host "   Frontend: http://localhost:5173"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "`nYou can close this window. Backend and Frontend are running in separate terminals."

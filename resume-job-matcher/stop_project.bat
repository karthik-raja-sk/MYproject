@echo off
TITLE AI Resume-Job Matcher - Shutdown
echo ===================================================
echo 🛑 Shutting down AI Resume-Job Matcher ...
echo ===================================================

echo [1/2] Stopping Backend (uvicorn/python)...
taskkill /F /IM uvicorn.exe /T 2>nul
taskkill /F /FI "WINDOWTITLE eq Backend - FastAPI*" /T 2>nul

echo [2/2] Stopping Frontend (node/vite)...
taskkill /F /IM node.exe /T 2>nul
taskkill /F /FI "WINDOWTITLE eq Frontend - Vite*" /T 2>nul

echo ===================================================
echo ✅ All processes stopped successfully.
echo ===================================================
pause

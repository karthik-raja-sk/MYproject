#!/bin/bash

# ============================================
# STOP SCRIPT
# Stops all running services
# ============================================

echo "🛑 Stopping Resume-Job Matcher..."

# Stop backend
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        echo "✅ Backend stopped"
    fi
    rm .backend.pid
fi

# Stop frontend
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        echo "✅ Frontend stopped"
    fi
    rm .frontend.pid
fi

# Stop PostgreSQL
docker-compose down

echo "✅ All services stopped"

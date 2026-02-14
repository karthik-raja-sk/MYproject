#!/bin/bash

# ============================================
# ONE-CLICK START SCRIPT
# Starts both backend and frontend
# ============================================

set -e

echo "🚀 Starting Resume-Job Matcher..."

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
    echo "❌ Setup not complete. Please run ./setup.sh first"
    exit 1
fi

# Start PostgreSQL if not running
if ! docker-compose ps | grep -q "postgres.*Up"; then
    echo "🐳 Starting PostgreSQL..."
    docker-compose up -d postgres
    sleep 3
fi

# Kill any existing processes on ports 8000 and 5173
echo "🧹 Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

# Start backend in background
echo "🐍 Starting backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

sleep 3

# Start frontend in background
if [ -d "frontend/node_modules" ]; then
    echo "⚛️  Starting frontend..."
    cd frontend
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    sleep 3
    
    echo ""
    echo "✅ Application is running!"
    echo ""
    echo "🌐 Frontend: http://localhost:5173"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "📋 Logs:"
    echo "   Backend: tail -f backend.log"
    echo "   Frontend: tail -f frontend.log"
    echo ""
    echo "🛑 To stop: ./stop.sh"
    echo ""
    
    # Save PIDs for stopping later
    echo $BACKEND_PID > .backend.pid
    echo $FRONTEND_PID > .frontend.pid
    
else
    echo ""
    echo "✅ Backend is running!"
    echo ""
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "⚠️  Frontend not found. Install with: cd frontend && npm install"
    echo ""
    
    echo $BACKEND_PID > .backend.pid
fi

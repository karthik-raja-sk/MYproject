# 🚀 Quick Start Guide

## Step 1: Download the Project

Download and extract the `resume-job-matcher` folder.

## Step 2: Install Prerequisites

### Install Docker
- Windows/Mac: https://www.docker.com/products/docker-desktop
- Linux: `sudo apt install docker.io docker-compose`

### Install Python 3.11
- https://www.python.org/downloads/

### Install Node.js 18+
- https://nodejs.org/

## Step 3: Run Setup (ONE TIME ONLY)

```bash
cd resume-job-matcher
chmod +x setup.sh start.sh stop.sh
./setup.sh
```

This will:
- Install Python dependencies
- Install Node.js dependencies  
- Start PostgreSQL database
- Initialize database schema
- Seed sample job postings

**Time**: ~5-10 minutes (depending on your internet speed)

## Step 4: Start the Application

```bash
./start.sh
```

Wait 5-10 seconds, then open:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Step 5: Test It Out!

1. Drag and drop a PDF resume
2. Wait for processing (~10 seconds)
3. View your top job matches!

## Stopping the Application

```bash
./stop.sh
```

## Troubleshooting

### "Permission denied" error
```bash
chmod +x setup.sh start.sh stop.sh
```

### "Port 5432 already in use"
```bash
sudo lsof -i :5432
sudo kill -9 <PID>
```

### "Port 8000 already in use"
```bash
lsof -ti:8000 | xargs kill -9
```

### Python virtual environment issues
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Manual Start (Alternative)

If scripts don't work, start manually:

### Terminal 1 - Database
```bash
docker-compose up postgres
```

### Terminal 2 - Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Terminal 3 - Frontend
```bash
cd frontend
npm run dev
```

## Need Help?

Check `README.md` for detailed documentation!

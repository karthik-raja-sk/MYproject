#!/bin/bash

# ============================================
# ONE-CLICK SETUP SCRIPT
# Resume-Job Matcher Platform
# ============================================

set -e  # Exit on error

echo "🚀 Starting Resume-Job Matcher Setup..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker detected${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js not found. Installing frontend dependencies will be skipped.${NC}"
    echo "Install Node.js from: https://nodejs.org/"
    SKIP_FRONTEND=true
else
    echo -e "${GREEN}✅ Node.js detected ($(node --version))${NC}"
    SKIP_FRONTEND=false
fi

# Create uploads directory
echo "📁 Creating upload directory..."
mkdir -p backend/uploads

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend .env file..."
    cat > backend/.env << EOF
DATABASE_URL=postgresql://postgres:password@postgres:5432/resume_matcher
MAX_FILE_SIZE_MB=5
UPLOAD_DIR=./uploads
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
EOF
    echo -e "${GREEN}✅ Backend .env created${NC}"
else
    echo -e "${YELLOW}⚠️  Backend .env already exists, skipping...${NC}"
fi

# Setup frontend
if [ "$SKIP_FRONTEND" = false ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
fi

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check if PostgreSQL is running
if docker-compose ps | grep -q "postgres.*Up"; then
    echo -e "${GREEN}✅ PostgreSQL is running${NC}"
else
    echo -e "${RED}❌ PostgreSQL failed to start${NC}"
    exit 1
fi

# Install Python dependencies and start backend
echo "🐍 Setting up Python backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies (this may take a few minutes)..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Initialize database
echo "🗄️  Initializing database..."
python -c "
from app.database import init_db
init_db()
print('Database initialized successfully')
"

echo -e "${GREEN}✅ Database initialized${NC}"

# Seed sample jobs
echo "🌱 Seeding sample job postings..."
cat > seed_jobs.py << 'SEED_EOF'
import sys
sys.path.insert(0, '.')
from app.database import SessionLocal, init_db
from app import models
from app.ai_logic import AIMatchingEngine

init_db()

sample_jobs = [
    {
        "title": "Senior Python Developer",
        "company": "TechCorp India",
        "location": "Bangalore, India (Remote)",
        "description": "We are looking for an experienced Python developer to join our backend team. You will work on building scalable APIs using FastAPI and microservices architecture. Strong knowledge of database optimization and cloud services required.",
        "requirements": "5+ years of Python experience, strong knowledge of FastAPI, PostgreSQL, Docker, and REST APIs. Experience with AWS is a plus.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST", "AWS"]
    },
    {
        "title": "Full Stack Developer",
        "company": "StartupHub",
        "location": "Mumbai, India",
        "description": "Join our fast-paced startup as a full-stack developer. Build modern web applications using React and Node.js. You'll work on both frontend and backend features.",
        "requirements": "3+ years experience with React, Node.js, Express, MongoDB. Experience with Tailwind CSS is preferred.",
        "required_skills": ["React", "Node.js", "Express", "MongoDB", "JavaScript", "Tailwind"]
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AI Solutions Ltd",
        "location": "Hyderabad, India",
        "description": "Work on cutting-edge ML projects using PyTorch and TensorFlow. Build and deploy ML models for production. Experience with NLP and computer vision is highly valued.",
        "requirements": "Strong Python skills, experience with PyTorch/TensorFlow, NLP, and model deployment. PhD preferred.",
        "required_skills": ["Python", "Machine Learning", "PyTorch", "TensorFlow", "NLP", "Deep Learning"]
    },
    {
        "title": "Frontend Developer - React",
        "company": "WebDesign Pro",
        "location": "Pune, India (Hybrid)",
        "description": "Create beautiful, responsive web interfaces using React and modern CSS frameworks. Collaborate with designers and backend developers.",
        "requirements": "2+ years React experience, strong CSS skills, experience with Tailwind or Bootstrap.",
        "required_skills": ["React", "JavaScript", "CSS", "Tailwind", "HTML", "TypeScript"]
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudOps Inc",
        "location": "Delhi NCR, India",
        "description": "Manage cloud infrastructure, CI/CD pipelines, and containerized applications. Automate deployment processes and ensure high availability.",
        "requirements": "Experience with AWS/Azure, Docker, Kubernetes, Jenkins, and Terraform.",
        "required_skills": ["AWS", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Terraform"]
    },
    {
        "title": "Data Scientist",
        "company": "Analytics Hub",
        "location": "Chennai, India",
        "description": "Analyze large datasets and build predictive models. Work with business teams to derive insights and make data-driven decisions.",
        "requirements": "Strong Python, SQL, and statistical modeling skills. Experience with scikit-learn and pandas required.",
        "required_skills": ["Python", "Machine Learning", "SQL", "Pandas", "Statistics", "Scikit-learn"]
    }
]

db = SessionLocal()
ai_engine = AIMatchingEngine()

try:
    for job_data in sample_jobs:
        # Generate embedding
        full_text = f"{job_data['title']} {job_data['description']} {job_data['requirements']}"
        embedding = ai_engine.generate_embedding(full_text)
        
        job = models.JobPosting(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            description=job_data["description"],
            requirements=job_data["requirements"],
            required_skills=job_data["required_skills"],
            embedding=embedding,
            is_active=True
        )
        db.add(job)
    
    db.commit()
    print(f"✅ Seeded {len(sample_jobs)} job postings")
except Exception as e:
    print(f"❌ Error seeding jobs: {e}")
finally:
    db.close()
SEED_EOF

python seed_jobs.py
rm seed_jobs.py

cd ..

echo ""
echo "========================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "========================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1️⃣  Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""

if [ "$SKIP_FRONTEND" = false ]; then
    echo "2️⃣  Start the frontend (in a new terminal):"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
fi

echo "3️⃣  Open your browser:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🎯 Or run the quick start script:"
echo "   ./start.sh"
echo ""
echo "========================================"

# 🎯 AI Resume-Job Matcher

An intelligent resume-job matching platform using **Semantic AI** and **NLP** to help job seekers find their perfect career fit.

![Status](https://img.shields.io/badge/status-ready-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18.2-61dafb)

## 🚀 One-Click Setup

```bash
# Make scripts executable
chmod +x setup.sh start.sh stop.sh

# Run setup (one time only)
./setup.sh

# Start the application
./start.sh
```

That's it! Open http://localhost:5173 in your browser 🎉

## 📋 Prerequisites

- **Docker** (for PostgreSQL)
- **Python 3.11+**
- **Node.js 18+**
- **8GB RAM** (for AI model)

## 🏗️ Architecture

### Clean Architecture Layers:
```
┌─────────────────────────────────────┐
│   Frontend (React + Tailwind)      │  ← Presentation Layer
├─────────────────────────────────────┤
│   FastAPI Routes (main.py)          │  ← API Layer
├─────────────────────────────────────┤
│   Business Logic (Services)         │  ← Application Layer
│   - parser.py (PDF Processing)      │
│   - ai_logic.py (ML Matching)       │
├─────────────────────────────────────┤
│   Data Models (SQLAlchemy)          │  ← Domain Layer
├─────────────────────────────────────┤
│   Database (PostgreSQL)             │  ← Infrastructure Layer
└─────────────────────────────────────┘
```

## 🎯 Key Features

- ✅ Drag-and-drop PDF upload
- ✅ AI-powered semantic matching
- ✅ Skill gap analysis
- ✅ Real-time progress indicators
- ✅ Comprehensive error handling
- ✅ Responsive UI
- ✅ Clean architecture
- ✅ Docker support
- ✅ RESTful API

## 📊 AI Matching Algorithm

### 1. Embedding Generation
- Model: `all-MiniLM-L6-v2` (384-dimensional vectors)
- Runs locally on CPU (no API costs)
- Generates embeddings for resume text and job descriptions

### 2. Score Calculation
```
Overall Score = (60% × Semantic Similarity) + (40% × Skill Match)

Where:
- Semantic Similarity: Cosine similarity of embeddings (0-1)
- Skill Match: Jaccard similarity of skills (0-100%)
```

### 3. Match Quality Thresholds
- **Excellent**: 80-100%
- **Good**: 60-79%
- **Fair**: 40-59%
- **Stretch**: 0-39%

## 🔧 Manual Setup (if scripts don't work)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL
docker-compose up -d postgres

# Run backend
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📝 API Endpoints

### Resume Upload
```
POST /api/resumes/upload
Content-Type: multipart/form-data
```

### Create Job
```
POST /api/jobs
Content-Type: application/json
```

### Generate Matches
```
POST /api/matches/{resume_id}
```

### Get Matches
```
GET /api/resumes/{resume_id}/matches
```

## 🧪 Testing

Upload a sample resume and watch the magic happen!

Sample job postings are automatically seeded during setup.

## 📦 Tech Stack

**Backend:**
- FastAPI (Web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- PyMuPDF (PDF parsing)
- Sentence-Transformers (AI)
- Scikit-learn (ML utilities)

**Frontend:**
- React 18
- Vite (Build tool)
- TailwindCSS (Styling)
- Axios (HTTP client)

## 🎓 For Professors

### Clean Architecture Explained:
1. **Separation of Concerns**: Each layer has a single responsibility
2. **Dependency Rule**: Inner layers don't know about outer layers
3. **Testability**: Business logic is independent of frameworks
4. **Maintainability**: Easy to modify without breaking other parts

### AI Model Choice:
- **Local execution**: No external API dependencies
- **Efficiency**: 384-dim vectors vs 1536-dim (OpenAI)
- **Cost**: Free, no API keys needed
- **Performance**: Runs on CPU in ~200ms per resume

## 🛑 Stopping the Application

```bash
./stop.sh
```

## 📄 License

MIT License - Free for educational use

## 🤝 Contributing

This is a mini-project for academic purposes.

---

**Built with ❤️ for B.Tech IT Mini-Project**

Need help? Check the docs/ folder for detailed guides!

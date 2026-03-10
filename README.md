# 🎯 AI Resume-Job Matcher

An intelligent resume-job matching platform using **Semantic AI** and **NLP** to help job seekers find their perfect career fit.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/React-18.2-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.100+-009688.svg)](https://fastapi.tiangolo.com/)

---

## ✨ Overview

This project is a full-stack application designed to bridge the gap between job seekers and recruiters. It uses **Sentence-Transformers** to perform semantic analysis on resumes and job descriptions, providing a more accurate matching score than simple keyword searches.

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance web framework for building APIs with Python.
- **SQLAlchemy**: SQL toolkit and Object Relational Mapper (ORM) for Python.
- **PostgreSQL**: Robust, scalable, and open-source relational database.
- **Sentence-Transformers**: State-of-the-art NLP model (`all-MiniLM-L6-v2`) for semantic embeddings.
- **PyMuPDF**: For fast and accurate PDF text extraction.

### Frontend
- **React 18**: Modern UI library for building dynamic interfaces.
- **Vite**: Next-generation frontend tooling for fast development and builds.
- **TailwindCSS**: Utility-first CSS framework for rapid UI development.
- **Axios**: Promised-based HTTP client for the browser.

---

## 🚀 Quick Start (Local Setup)

The easiest way to get started on Windows is to use the provided setup and start scripts.

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL** (running locally or via Docker)

### 2. One-Click Setup
```powershell
# Run the setup script to install dependencies and configure the environment
.\setup_project.bat
```

### 3. Start the Project
```powershell
# Start both backend and frontend servers
.\run_project.bat
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🏗️ Architecture

The project follows a **Clean Architecture** pattern, ensuring separation of concerns and maintainability.

```
AI Resume-Job Matcher
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── routes/         # API Endpoints
│   │   ├── services/       # Business Logic (AI, Parsing)
│   │   ├── models.py       # SQLAlchemy Models
│   │   └── config.py       # Configuration
│   └── requirements.txt    # Python Dependencies
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # UI Components
│   │   ├── pages/          # Application Views
│   │   └── App.jsx         # Main Component
│   └── package.json        # Node.js Dependencies
└── docker-compose.yml      # Infrastructure Setup
```

---

## 📊 How it Works

1. **Upload**: Users upload their resume in PDF format.
2. **Parsing**: The backend extracts text and identifies key skills using NLP.
3. **Semantic Matching**:
   - The system generates embeddings for the resume and available job descriptions.
   - It calculates **Cosine Similarity** between the vectors.
   - A final score is weighted: `(60% Semantic) + (40% Skill Match)`.
4. **Insights**: The UI displays a match percentage, skill gap analysis, and recommendations.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for AI-based Recruitment Automation.**

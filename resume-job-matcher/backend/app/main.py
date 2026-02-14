"""
FastAPI main application.
RESTful API for resume upload and job matching.
"""
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import logging
from pathlib import Path

from .database import get_db, init_db, engine
from .config import get_settings
from . import models, schemas
from .parser import ResumeParser
from .ai_logic import AIMatchingEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume-Job Matcher API",
    description="AI-powered semantic resume-job matching system",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load settings
settings = get_settings()

# Initialize AI engine (singleton)
ai_engine = AIMatchingEngine(model_name=settings.model_name)

# Initialize parser
resume_parser = ResumeParser()

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "message": "Resume-Job Matcher API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post(
    "/api/resumes/upload",
    response_model=schemas.ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a resume PDF.
    
    Edge cases handled:
    - File size validation (max 5MB)
    - File type validation (only PDF)
    - Empty PDFs
    - Corrupted PDFs
    """
    # Validate file extension
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    # Validate file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    max_size_bytes = settings.max_file_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds {settings.max_file_size_mb}MB limit"
        )
    
    # Edge case: Empty file
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )
    
    # Save file temporarily
    file_path = os.path.join(settings.upload_dir, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Parse PDF
    try:
        parsed_data = resume_parser.parse_pdf(file_path)
    except ValueError as e:
        # Clean up file
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Clean up file
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse PDF: {str(e)}"
        )
    
    # Generate AI embedding
    try:
        embedding = ai_engine.generate_embedding(parsed_data["raw_text"])
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embedding: {str(e)}"
        )
    
    # Save to database
    resume = models.Resume(
        filename=file.filename,
        file_size=file_size,
        raw_text=parsed_data["raw_text"],
        parsed_skills=parsed_data["parsed_skills"],
        parsed_experience=parsed_data["parsed_experience"],
        embedding=embedding,
        processing_status="completed"
    )
    
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    logger.info(f"Resume uploaded successfully: ID={resume.id}, Skills={len(parsed_data['parsed_skills'])}")
    
    return schemas.ResumeUploadResponse(
        id=resume.id,
        filename=resume.filename,
        file_size=resume.file_size,
        processing_status=resume.processing_status,
        message=f"Resume processed successfully. Extracted {len(parsed_data['parsed_skills'])} skills."
    )


@app.post(
    "/api/jobs",
    response_model=schemas.JobPostingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_job(
    job: schemas.JobPostingCreate,
    db: Session = Depends(get_db)
):
    """Create a new job posting."""
    # Generate embedding for job description
    full_text = f"{job.title} {job.description} {job.requirements or ''}"
    embedding = ai_engine.generate_embedding(full_text)
    
    # Create job posting
    db_job = models.JobPosting(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        requirements=job.requirements,
        required_skills=job.required_skills,
        embedding=embedding
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    logger.info(f"Job created: ID={db_job.id}, Title={db_job.title}")
    
    return db_job


@app.get("/api/jobs", response_model=List[schemas.JobPostingResponse])
def list_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all job postings."""
    jobs = db.query(models.JobPosting).filter(
        models.JobPosting.is_active == True
    ).offset(skip).limit(limit).all()
    
    return jobs


@app.post("/api/matches/{resume_id}", response_model=schemas.MatchListResponse)
def generate_matches(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered matches between a resume and all active jobs.
    Returns sorted list of matches (best matches first).
    """
    # Get resume
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    
    # Get all active jobs
    jobs = db.query(models.JobPosting).filter(models.JobPosting.is_active == True).all()
    
    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active job postings found"
        )
    
    # Delete existing matches for this resume
    db.query(models.Match).filter(models.Match.resume_id == resume_id).delete()
    
    matches = []
    
    for job in jobs:
        # Calculate semantic similarity
        semantic_sim = ai_engine.calculate_similarity(resume.embedding, job.embedding)
        
        # Calculate skill match
        skill_match_score, matching_skills, missing_skills = ai_engine.calculate_skill_match(
            resume.parsed_skills or [],
            job.required_skills or []
        )
        
        # Calculate overall score
        overall_score = ai_engine.calculate_overall_score(semantic_sim, skill_match_score)
        
        # Generate explanation
        explanation = ai_engine.generate_match_explanation(
            overall_score,
            semantic_sim,
            skill_match_score,
            matching_skills,
            missing_skills
        )
        
        # Only save matches above threshold
        if overall_score >= (settings.similarity_threshold * 100):
            match = models.Match(
                resume_id=resume.id,
                job_id=job.id,
                overall_score=overall_score,
                semantic_similarity=semantic_sim,
                skill_match_score=skill_match_score,
                matching_skills=matching_skills,
                missing_skills=missing_skills,
                explanation=explanation
            )
            
            db.add(match)
            matches.append(match)
    
    db.commit()
    
    # Refresh all matches to get IDs
    for match in matches:
        db.refresh(match)
    
    # Sort by overall score (best first)
    matches.sort(key=lambda m: m.overall_score, reverse=True)
    
    # Format response
    match_responses = []
    for match in matches:
        match_responses.append(schemas.MatchResponse(
            id=match.id,
            job_id=match.job_id,
            job_title=match.job.title,
            company=match.job.company,
            location=match.job.location,
            overall_score=match.overall_score,
            semantic_similarity=match.semantic_similarity,
            skill_match_score=match.skill_match_score,
            matching_skills=match.matching_skills,
            missing_skills=match.missing_skills,
            explanation=match.explanation,
            matched_at=match.matched_at
        ))
    
    logger.info(f"Generated {len(matches)} matches for resume ID {resume_id}")
    
    return schemas.MatchListResponse(
        resume_id=resume.id,
        resume_filename=resume.filename,
        total_matches=len(match_responses),
        matches=match_responses
    )


@app.get("/api/resumes/{resume_id}/matches", response_model=schemas.MatchListResponse)
def get_resume_matches(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """Get all existing matches for a resume."""
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    
    matches = db.query(models.Match).filter(
        models.Match.resume_id == resume_id
    ).order_by(models.Match.overall_score.desc()).all()
    
    match_responses = []
    for match in matches:
        match_responses.append(schemas.MatchResponse(
            id=match.id,
            job_id=match.job_id,
            job_title=match.job.title,
            company=match.job.company,
            location=match.job.location,
            overall_score=match.overall_score,
            semantic_similarity=match.semantic_similarity,
            skill_match_score=match.skill_match_score,
            matching_skills=match.matching_skills,
            missing_skills=match.missing_skills,
            explanation=match.explanation,
            matched_at=match.matched_at
        ))
    
    return schemas.MatchListResponse(
        resume_id=resume.id,
        resume_filename=resume.filename,
        total_matches=len(match_responses),
        matches=match_responses
    )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return schemas.ErrorResponse(
        error=exc.detail,
        detail=str(exc.status_code)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models
from ..services.match_service import MatchService
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/matches", tags=["matches"])
match_service = MatchService()

@router.post("/run/{resume_id}", response_model=List[schemas.MatchResponse])
def run_matching(
    resume_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    results = match_service.run_matching(db, resume_id, current_user.id)
    if results is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return results

@router.get("/history", response_model=List[schemas.MatchResponse])
def get_match_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    matches = match_service.get_user_match_history(db, current_user.id)
    
    # We need to map the DB models to the detailed MatchResponse schema which includes job info
    # In a real app, we'd use a more efficient join query in the service
    history = []
    for m in matches:
        job = m.job
        history.append({
            "job_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "location": job.location,
            "overall_score": m.overall_score,
            "semantic_similarity": m.semantic_similarity,
            "skill_match_score": m.skill_match_score,
            "matching_skills": m.matching_skills,
            "missing_skills": m.missing_skills,
            "explanation": m.explanation
        })
    return history

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    total_resumes = db.query(models.Resume).filter(models.Resume.user_id == current_user.id).count()
    total_matches = db.query(models.Match).filter(models.Match.user_id == current_user.id).count()
    
    best_match = db.query(models.Match).filter(
        models.Match.user_id == current_user.id
    ).order_by(models.Match.overall_score.desc()).first()
    
    best_score = best_match.overall_score if best_match else 0
    
    return {
        "total_resumes": total_resumes,
        "total_matches": total_matches,
        "best_score": best_score,
        "username": current_user.full_name or current_user.email
    }

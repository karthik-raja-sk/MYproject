from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models
from ..services import job_service
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.post("/create", response_model=schemas.JobPostingResponse)
def create_job(
    job: schemas.JobPostingCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return job_service.create_job(db, job)

@router.get("/list", response_model=List[schemas.JobPostingResponse])
def list_jobs(db: Session = Depends(get_db)):
    return job_service.get_jobs(db)

@router.delete("/{job_id}")
def delete_job(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    success = job_service.delete_job(db, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}

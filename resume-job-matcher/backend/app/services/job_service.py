from sqlalchemy.orm import Session
from .. import models, schemas
from ..ai.embedding_service import get_embedding_service

embedding_service = get_embedding_service()

def create_job(db: Session, job: schemas.JobPostingCreate):
    # Combine title, description and requirements for embedding
    full_text = f"{job.title} {job.description} {job.requirements or ''}"
    embedding = embedding_service.generate_embedding(full_text)
    
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
    return db_job

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobPosting).filter(models.JobPosting.is_active == True).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int):
    return db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()

def delete_job(db: Session, job_id: int):
    db_job = get_job(db, job_id)
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False

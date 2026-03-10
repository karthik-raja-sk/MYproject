from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models
from ..services import resume_service
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/resumes", tags=["resumes"])

@router.post("/upload", response_model=schemas.ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    return resume_service.create_resume(db, file, current_user.id)

@router.get("/list", response_model=List[schemas.ResumeResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return resume_service.get_user_resumes(db, current_user.id)

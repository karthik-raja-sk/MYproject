import os
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils.parser import PDFParser
from ..utils.skill_extractor import SkillExtractor
from ..ai.embedding_service import get_embedding_service
from ..config import get_settings

settings = get_settings()
pdf_parser = PDFParser()
skill_extractor = SkillExtractor()
embedding_service = get_embedding_service()

def create_resume(db: Session, file: UploadFile, user_id: int):
    # Ensure upload directory exists
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    file_path = os.path.join(settings.upload_dir, file.filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Parse content
        raw_text = pdf_parser.extract_text(file_path)
        skills = skill_extractor.extract_skills(raw_text)
        experience = skill_extractor.extract_experience(raw_text)
        
        # Generate embedding
        embedding = embedding_service.generate_embedding(raw_text)
        
        # Save to DB
        db_resume = models.Resume(
            user_id=user_id,
            filename=file.filename,
            file_size=os.path.getsize(file_path),
            raw_text=raw_text,
            parsed_skills=skills,
            parsed_experience=experience,
            embedding=embedding,
            processing_status="completed"
        )
        
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        
        return db_resume
    
    except Exception as e:
        # Cleanup if failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

def get_user_resumes(db: Session, user_id: int):
    return db.query(models.Resume).filter(models.Resume.user_id == user_id).all()

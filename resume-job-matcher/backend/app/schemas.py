from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Any
from datetime import datetime

# Auth Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Resume Schemas
class ResumeBase(BaseModel):
    filename: str

class ResumeUploadResponse(ResumeBase):
    id: int
    file_size: int
    processing_status: str
    message: str

class ResumeResponse(ResumeBase):
    id: int
    upload_date: datetime
    parsed_skills: List[str]
    processing_status: str

    class Config:
        from_attributes = True

# Job Schemas
class JobPostingBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    required_skills: List[str] = []

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingResponse(JobPostingBase):
    id: int
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Match Schemas
class MatchResponse(BaseModel):
    job_id: int
    job_title: str
    company: str
    location: Optional[str] = None
    overall_score: float
    semantic_similarity: float
    skill_match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str

class MatchListResponse(BaseModel):
    resume_id: int
    resume_filename: str
    total_matches: int
    matches: List[MatchResponse]

# Generic
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

"""
Pydantic schemas for request/response validation.
Separates API contracts from database models (clean architecture).
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class ResumeUploadResponse(BaseModel):
    """Response after successful resume upload."""
    id: int
    filename: str
    file_size: int
    processing_status: str
    message: str
    
    class Config:
        from_attributes = True


class SkillBase(BaseModel):
    """Individual skill representation."""
    name: str
    confidence: Optional[float] = None


class JobPostingCreate(BaseModel):
    """Schema for creating a new job posting."""
    title: str = Field(..., min_length=5, max_length=500)
    company: str = Field(..., min_length=2, max_length=255)
    location: str = Field(..., max_length=255)
    description: str = Field(..., min_length=50)
    requirements: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)


class JobPostingResponse(BaseModel):
    """Job posting response schema."""
    id: int
    title: str
    company: str
    location: str
    description: str
    required_skills: List[str]
    created_date: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class MatchResponse(BaseModel):
    """Individual match result."""
    id: int
    job_id: int
    job_title: str
    company: str
    location: str
    overall_score: float
    semantic_similarity: float
    skill_match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str
    matched_at: datetime
    
    class Config:
        from_attributes = True


class MatchListResponse(BaseModel):
    """List of matches for a resume."""
    resume_id: int
    resume_filename: str
    total_matches: int
    matches: List[MatchResponse]


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

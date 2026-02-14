"""
SQLAlchemy ORM models for database tables.
Clean architecture: Models are independent of business logic.
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Resume(Base):
    """User's uploaded resume with parsed content."""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer)  # in bytes
    
    # Parsed content
    raw_text = Column(Text, nullable=False)
    parsed_skills = Column(JSON)  # List of extracted skills
    parsed_experience = Column(JSON)  # Structured experience data
    
    # AI embeddings (stored as JSON array for simplicity)
    embedding = Column(JSON)  # 384-dimensional vector from all-MiniLM-L6-v2
    
    # Metadata
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    processing_status = Column(String(50), default="pending")  # pending, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Relationships
    matches = relationship("Match", back_populates="resume", cascade="all, delete-orphan")


class JobPosting(Base):
    """Job posting with requirements and description."""
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    
    # Job details
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    required_skills = Column(JSON)  # List of required skills
    
    # AI embeddings
    embedding = Column(JSON)  # 384-dimensional vector
    
    # Metadata
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    matches = relationship("Match", back_populates="job", cascade="all, delete-orphan")


class Match(Base):
    """AI-generated resume-job match with scores."""
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    
    # Matching scores
    overall_score = Column(Float, nullable=False)  # 0-100
    semantic_similarity = Column(Float)  # Cosine similarity (0-1)
    skill_match_score = Column(Float)  # Percentage of required skills matched
    
    # Analysis
    matching_skills = Column(JSON)  # Skills user has that match job
    missing_skills = Column(JSON)  # Skills user lacks
    explanation = Column(Text)  # Human-readable match explanation
    
    # Metadata
    matched_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    resume = relationship("Resume", back_populates="matches")
    job = relationship("JobPosting", back_populates="matches")

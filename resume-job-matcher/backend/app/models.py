from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="user", cascade="all, delete-orphan")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer)
    raw_text = Column(Text, nullable=False)
    parsed_skills = Column(JSON)
    parsed_experience = Column(JSON)
    embedding = Column(JSON)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    processing_status = Column(String(50), default="pending")
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    matches = relationship("Match", back_populates="resume", cascade="all, delete-orphan")

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    required_skills = Column(JSON)
    embedding = Column(JSON)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    matches = relationship("Match", back_populates="job", cascade="all, delete-orphan")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    
    overall_score = Column(Float, nullable=False)
    semantic_similarity = Column(Float)
    skill_match_score = Column(Float)
    matching_skills = Column(JSON)
    missing_skills = Column(JSON)
    explanation = Column(Text)
    matched_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="matches")
    resume = relationship("Resume", back_populates="matches")
    job = relationship("JobPosting", back_populates="matches")

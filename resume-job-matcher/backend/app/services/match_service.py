from sqlalchemy.orm import Session
from .. import models
from ..ai.ai_logic import AILogic

ai_logic = AILogic()

class MatchService:
    def run_matching(self, db: Session, resume_id: int, user_id: int):
        """Run matching for a specific resume against all active jobs."""
        resume = db.query(models.Resume).filter(
            models.Resume.id == resume_id, 
            models.Resume.user_id == user_id
        ).first()
        
        if not resume:
            return None
            
        jobs = db.query(models.JobPosting).filter(models.JobPosting.is_active == True).all()
        
        results = []
        for job in jobs:
            # Semantic Similarity
            semantic_sim = ai_logic.calculate_similarity(resume.embedding, job.embedding)
            
            # Skill Match
            skill_score, matching_skills, missing_skills = ai_logic.calculate_skill_overlap(
                resume.parsed_skills or [], 
                job.required_skills or []
            )
            
            # Weighted Overall Score
            overall_score = ai_logic.calculate_weighted_score(semantic_sim, skill_score)
            
            # Generate explanation
            explanation = ai_logic.generate_explanation(overall_score, matching_skills, missing_skills)
            
            # Update or create match
            existing_match = db.query(models.Match).filter(
                models.Match.resume_id == resume_id,
                models.Match.job_id == job.id
            ).first()
            
            if existing_match:
                existing_match.overall_score = overall_score
                existing_match.semantic_similarity = semantic_sim
                existing_match.skill_match_score = skill_score
                existing_match.matching_skills = matching_skills
                existing_match.missing_skills = missing_skills
                existing_match.explanation = explanation
                db.add(existing_match)
            else:
                match = models.Match(
                    user_id=user_id,
                    resume_id=resume_id,
                    job_id=job.id,
                    overall_score=overall_score,
                    semantic_similarity=semantic_sim,
                    skill_match_score=skill_score,
                    matching_skills=matching_skills,
                    missing_skills=missing_skills,
                    explanation=explanation
                )
                db.add(match)
            
            results.append({
                "job_id": job.id,
                "job_title": job.title,
                "company": job.company,
                "location": job.location,
                "overall_score": overall_score,
                "semantic_similarity": semantic_sim,
                "skill_match_score": skill_score,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "explanation": explanation
            })
            
        db.commit()
        return results

    def get_user_match_history(self, db: Session, user_id: int):
        return db.query(models.Match).filter(models.Match.user_id == user_id).order_by(models.Match.matched_at.desc()).all()

    def get_user_match_history(self, db: Session, user_id: int):
        return db.query(models.Match).filter(models.Match.user_id == user_id).order_by(models.Match.matched_at.desc()).all()

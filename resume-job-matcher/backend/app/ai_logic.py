"""
AI matching engine using Sentence Transformers.
Runs locally on CPU - no API keys needed.
"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class AIMatchingEngine:
    """
    Semantic similarity matching using Sentence-BERT.
    Uses all-MiniLM-L6-v2 model (lightweight, runs on CPU).
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the model (download on first run)."""
        logger.info(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info("Model loaded successfully")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate 384-dimensional embedding for text.
        
        Args:
            text: Input text (resume or job description)
            
        Returns:
            List of floats representing the embedding
        """
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty text")
        
        # Generate embedding
        embedding = self.model.encode(text, convert_to_tensor=False)
        
        # Convert to list for JSON serialization
        return embedding.tolist()
    
    def calculate_similarity(
        self, 
        embedding1: List[float], 
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Returns:
            Float between 0 and 1 (1 = identical, 0 = completely different)
        """
        # Convert to numpy arrays
        emb1 = np.array(embedding1).reshape(1, -1)
        emb2 = np.array(embedding2).reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(emb1, emb2)[0][0]
        
        return float(similarity)
    
    def calculate_skill_match(
        self,
        resume_skills: List[str],
        required_skills: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        """
        Calculate skill overlap between resume and job requirements.
        
        Returns:
            Tuple of (match_percentage, matching_skills, missing_skills)
        """
        if not required_skills:
            return 100.0, resume_skills, []
        
        # Normalize skills to lowercase for comparison
        resume_skills_lower = {s.lower() for s in resume_skills}
        required_skills_lower = {s.lower() for s in required_skills}
        
        # Find matches
        matching = resume_skills_lower.intersection(required_skills_lower)
        missing = required_skills_lower - resume_skills_lower
        
        # Calculate percentage
        match_percentage = (len(matching) / len(required_skills_lower)) * 100
        
        # Convert back to original case for display
        matching_skills = [s for s in resume_skills if s.lower() in matching]
        missing_skills = [s for s in required_skills if s.lower() in missing]
        
        return match_percentage, matching_skills, missing_skills
    
    def generate_match_explanation(
        self,
        overall_score: float,
        semantic_similarity: float,
        skill_match_score: float,
        matching_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """
        Generate human-readable explanation of the match.
        """
        # Determine match quality
        if overall_score >= 80:
            quality = "Excellent"
        elif overall_score >= 60:
            quality = "Good"
        elif overall_score >= 40:
            quality = "Fair"
        else:
            quality = "Weak"
        
        explanation = f"{quality} match ({overall_score:.1f}% overall). "
        
        # Semantic similarity feedback
        if semantic_similarity >= 0.7:
            explanation += "Your resume content strongly aligns with the job description. "
        elif semantic_similarity >= 0.5:
            explanation += "Your resume shows moderate alignment with the job requirements. "
        else:
            explanation += "Your resume shows limited alignment with this role. "
        
        # Skill match feedback
        if skill_match_score >= 80:
            explanation += f"You have {len(matching_skills)}/{len(matching_skills) + len(missing_skills)} required skills. "
        elif skill_match_score >= 50:
            explanation += f"You have {len(matching_skills)} matching skills, but missing {len(missing_skills)} key skills. "
        else:
            explanation += f"Significant skill gap: missing {len(missing_skills)} required skills. "
        
        # Missing skills recommendation
        if missing_skills:
            top_missing = missing_skills[:3]
            explanation += f"Consider learning: {', '.join(top_missing)}."
        
        return explanation
    
    def calculate_overall_score(
        self,
        semantic_similarity: float,
        skill_match_score: float
    ) -> float:
        """
        Calculate weighted overall match score.
        
        Formula: 60% semantic similarity + 40% skill match
        """
        # Semantic similarity is 0-1, convert to 0-100
        semantic_score = semantic_similarity * 100
        
        # Weighted average
        overall = (0.6 * semantic_score) + (0.4 * skill_match_score)
        
        return round(overall, 2)

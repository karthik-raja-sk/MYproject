import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

class AILogic:
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        if not embedding1 or not embedding2:
            return 0.0
        
        emb1 = np.array(embedding1).reshape(1, -1)
        emb2 = np.array(embedding2).reshape(1, -1)
        
        similarity = cosine_similarity(emb1, emb2)[0][0]
        return float(similarity)

    def calculate_skill_overlap(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """Calculate skill matching percentage and identify gaps."""
        if not job_skills:
            return 100.0, resume_skills, []
            
        resume_set = {s.lower() for s in resume_skills}
        job_set = {s.lower() for s in job_skills}
        
        matching = job_set.intersection(resume_set)
        missing = job_set - resume_set
        
        score = (len(matching) / len(job_set)) * 100
        
        return score, list(matching), list(missing)

    def calculate_weighted_score(self, semantic_similarity: float, skill_score: float) -> float:
        """Weighted average: 60% semantic, 40% skills."""
        return (0.6 * (semantic_similarity * 100)) + (0.4 * skill_score)

    def generate_explanation(self, score: float, matching: List[str], missing: List[str]) -> str:
        if score >= 80:
            quality = "Excellent"
        elif score >= 60:
            quality = "Good"
        elif score >= 40:
            quality = "Fair"
        else:
            quality = "Weak"
            
        explanation = f"{quality} match ({score:.1f}%). "
        if matching:
            explanation += f"You have strong skills in {', '.join(matching[:3])}. "
        if missing:
            explanation += f"Consider improving your knowledge in {', '.join(missing[:3])} to better fit this role."
            
        return explanation

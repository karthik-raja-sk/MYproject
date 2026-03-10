import re
from typing import List

class SkillExtractor:
    def __init__(self):
        # Basic common skills list (can be expanded)
        self.skill_keywords = [
            "python", "java", "javascript", "react", "node", "sql", "postgresql",
            "machine learning", "deep learning", "fastapi", "docker", "aws",
            "tensorflow", "pytorch", "html", "css", "git", "rest api", "nosql",
            "mongodb", "redis", "kubernetes", "typescript", "angular", "vue",
            "next.js", "django", "flask", "spring boot", "c++", "c#", "go", "rust"
        ]

    def extract_skills(self, text: str) -> List[str]:
        """Simple regex-based skill extraction."""
        text_lower = text.lower()
        found_skills = set()
        
        for skill in self.skill_keywords:
            # Use word boundaries to avoid partial matches (e.g., 'java' in 'javascript')
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        return list(found_skills)

    def extract_experience(self, text: str) -> str:
        """Basic experience extraction."""
        pattern = r"\d+\+?\s*(years|yrs)\s*(of)?\s*experience"
        matches = re.findall(pattern, text.lower())
        return matches[0] if matches else "Not specified"

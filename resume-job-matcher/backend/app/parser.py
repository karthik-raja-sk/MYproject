"""
PDF parsing logic using PyMuPDF.
Handles edge cases: empty PDFs, corrupted files, large files.
"""
import fitz  # PyMuPDF
import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ResumeParser:
    """Extracts text and structured data from PDF resumes."""
    
    # Common skill patterns (can be expanded)
    SKILL_PATTERNS = [
        r'\b(Python|Java|JavaScript|TypeScript|C\+\+|C#|Ruby|Go|Rust|Swift|Kotlin)\b',
        r'\b(React|Angular|Vue|Node\.js|Express|Django|Flask|FastAPI|Spring)\b',
        r'\b(PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch|DynamoDB)\b',
        r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|CI/CD)\b',
        r'\b(Machine Learning|Deep Learning|NLP|Computer Vision|TensorFlow|PyTorch)\b',
        r'\b(HTML|CSS|Tailwind|Bootstrap|REST|GraphQL|WebSocket)\b',
    ]
    
    def parse_pdf(self, file_path: str) -> Dict:
        """
        Extract text and metadata from PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with raw_text, skills, and metadata
            
        Raises:
            ValueError: If PDF is empty or corrupted
        """
        try:
            doc = fitz.open(file_path)
            
            # Edge case: Empty PDF
            if doc.page_count == 0:
                raise ValueError("PDF file is empty (0 pages)")
            
            # Extract text from all pages
            raw_text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                raw_text += page.get_text()
            
            doc.close()
            
            # Edge case: PDF with no extractable text (might be scanned image)
            if not raw_text.strip():
                raise ValueError(
                    "No text could be extracted from PDF. "
                    "It might be a scanned image or corrupted file."
                )
            
            # Clean text
            raw_text = self._clean_text(raw_text)
            
            # Extract skills
            skills = self._extract_skills(raw_text)
            
            # Extract experience (basic implementation)
            experience = self._extract_experience(raw_text)
            
            return {
                "raw_text": raw_text,
                "parsed_skills": skills,
                "parsed_experience": experience,
                "page_count": doc.page_count,
                "char_count": len(raw_text)
            }
            
        except fitz.fitz.FileDataError as e:
            raise ValueError(f"Corrupted or invalid PDF file: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Remove extra whitespace and normalize text."""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\-\(\)\@\#\+]', '', text)
        return text.strip()
    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills using regex patterns.
        Returns deduplicated list of skills.
        """
        skills = set()
        
        for pattern in self.SKILL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update([m.strip() for m in matches])
        
        # Convert to sorted list for consistency
        return sorted(list(skills), key=str.lower)
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """
        Basic experience extraction (looks for year patterns).
        This is a simplified implementation - can be enhanced with NER.
        """
        experience = []
        
        # Look for year ranges (e.g., "2020-2023", "2020 - Present")
        year_pattern = r'(\d{4})\s*[-–]\s*(\d{4}|Present|Current)'
        matches = re.findall(year_pattern, text, re.IGNORECASE)
        
        for start, end in matches:
            experience.append({
                "start_year": start,
                "end_year": end,
                "duration": self._calculate_duration(start, end)
            })
        
        return experience
    
    def _calculate_duration(self, start: str, end: str) -> str:
        """Calculate duration in years."""
        try:
            start_year = int(start)
            end_year = int(end) if end.isdigit() else 2024
            duration = end_year - start_year
            return f"{duration} years" if duration > 1 else f"{duration} year"
        except:
            return "Unknown"

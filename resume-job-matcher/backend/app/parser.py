"""
Resume PDF Parser
Extracts text and basic information from resumes
"""

import fitz  # PyMuPDF
import logging
import re

logger = logging.getLogger(__name__)


class ResumeParser:

    def parse_pdf(self, file_path: str):
        """
        Parse a PDF resume and extract text + skills
        """

        try:
            doc = fitz.open(file_path)

            text = ""

            for page in doc:
                text += page.get_text()

            page_count = len(doc)

            doc.close()

            if not text.strip():
                raise ValueError("PDF contains no readable text")

            skills = self.extract_skills(text)
            experience = self.extract_experience(text)

            return {
                "raw_text": text,
                "parsed_skills": skills,
                "parsed_experience": experience,
                "page_count": page_count
            }

        except fitz.FileDataError:
            raise ValueError("Invalid or corrupted PDF")

        except Exception as e:
            logger.error(f"PDF parsing failed: {e}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    def extract_skills(self, text: str):

        skill_keywords = [
            "python",
            "java",
            "javascript",
            "react",
            "node",
            "sql",
            "machine learning",
            "deep learning",
            "fastapi",
            "docker",
            "aws",
            "tensorflow",
            "pytorch",
            "html",
            "css",
            "git"
        ]

        text_lower = text.lower()

        skills_found = []

        for skill in skill_keywords:
            if skill in text_lower:
                skills_found.append(skill)

        return skills_found

    def extract_experience(self, text: str):

        pattern = r"\d+\+?\s*(years|yrs)"

        matches = re.findall(pattern, text.lower())

        return matches
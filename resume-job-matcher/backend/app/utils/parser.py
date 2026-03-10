import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            if not text.strip():
                raise ValueError("PDF contains no readable text")
            
            return text
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")

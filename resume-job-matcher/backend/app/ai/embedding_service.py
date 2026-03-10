from sentence_transformers import SentenceTransformer
import logging
from functools import lru_cache
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading SentenceTransformer model: {settings.model_name}")
            self._model = SentenceTransformer(settings.model_name)
            logger.info("Model loaded successfully")
        return self._model

    def generate_embedding(self, text: str):
        if not text or not text.strip():
            return None
        
        # Generate embedding and convert to list for storage
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

@lru_cache()
def get_embedding_service():
    return EmbeddingService()

from typing import Union, List
import numpy as np
from sentence_transformers import SentenceTransformer
from .feature_extractor import FeatureExtractor
from src.utils.logger import logger


class TextFeatureExtractor(FeatureExtractor):
    """Feature extractor using pretrained sentence transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: Union[str, None] = None):
        self.model_name = model_name
        super().__init__(device)
        self.model.eval()

    def _load_model(self):
        try:
            model = SentenceTransformer(self.model_name, device=str(self.device))
            feature_dim = model.get_sentence_embedding_dimension()
            logger.info(f"Loaded sentence transformer {self.model_name}")
            return model, feature_dim
        except Exception as e:
            logger.error(f"Failed to load sentence transformer model {self.model_name}: {e}")
            raise

    def _extract(self, text: Union[str, List[str], None]) -> np.ndarray:
        if text is None:
            logger.error("Received None text for feature extraction.")
            return np.array([])
        try:
            if isinstance(text, list):
                embeddings = self.model.encode(text)
            else:
                embeddings = self.model.encode([text])
            return np.array(embeddings).flatten()
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return np.array([])

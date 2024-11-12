import numpy as np
from typing import List, Tuple
from src.database.feature_database import FeatureDatabase
from src.utils.logger import logger
from src.config.settings import Settings


class SimilaritySearch:
    def __init__(self, database: FeatureDatabase):
        self.database = database
        logger.info("Similarity search initialized.")

    def find_similar(
        self, query_features: np.ndarray, k: int = Settings.K_NEIGHBORS
    ) -> Tuple[np.ndarray, np.ndarray]:
        if query_features.ndim != 2:
            logger.error("Query features should be a 2D array.")
            return np.array([]), np.array([])
        distances, indices = self.database.search(query_features, k)
        if distances.size == 0 and indices.size == 0:
            logger.warning("No results found during similarity search.")
        else:
            logger.info(f"Found {k} similar features for each query.")
        return distances, indices

    def get_labels(self, indices: np.ndarray) -> List[str]:
        labels = []
        logger.info(f"Retrieving labels for {indices.size} indices.")
        logger.info(f"Database labels: {self.database.labels}")
        logger.info(f"Indices: {indices.flatten()}")
        for idx in indices.flatten():
            if idx < len(self.database.labels):
                labels.append(self.database.labels[idx])
            else:
                logger.warning(f"Index {idx} is out of bounds.")
                labels.append("Unknown")
        return labels

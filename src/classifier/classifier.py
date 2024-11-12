from typing import List
from collections import Counter
import numpy as np
from src.search.similarity_search import SimilaritySearch
from src.utils.logger import logger
from src.config.settings import Settings


class Classifier:
    def __init__(self, similarity_search: SimilaritySearch):
        self.similarity_search = similarity_search
        logger.info("Classifier initialized.")

    def predict(self, query_features: np.ndarray, k: int = Settings.K_NEIGHBORS) -> str:
        distances, indices = self.similarity_search.find_similar(query_features, k)
        if indices.size == 0:
            logger.warning("No indices returned for prediction.")
            return "Unknown"
        labels = self.similarity_search.get_labels(indices)
        most_common = Counter(labels).most_common(1)
        predicted_label = most_common[0][0] if most_common else "Unknown"
        logger.info(
            f"Predicted label: {predicted_label} with confidence {most_common[0][1]} and distance {distances[0][0]}"
        )
        return predicted_label

    def predict_batch(
        self, query_features: np.ndarray, k: int = Settings.K_NEIGHBORS
    ) -> List[str]:
        distances, indices = self.similarity_search.find_similar(query_features, k)
        predicted_labels = []
        for idx in indices:
            labels = self.similarity_search.get_labels([idx])
            most_common = Counter(labels).most_common(1)
            predicted_label = most_common[0][0] if most_common else "Unknown"
            predicted_labels.append(predicted_label)
        logger.info(f"Predicted labels for batch: {predicted_labels}")
        return predicted_labels
